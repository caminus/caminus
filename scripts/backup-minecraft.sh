#!/bin/sh
trap exit SIGINT
MINECRAFT_HOME="/srv/minecraft/"
WORLD_DIR="$MINECRAFT_HOME/server"
BACKUP_DIR="$MINECRAFT_HOME/backup"
BACKUP_ARCHIVES="$BACKUP_DIR/archive"
BACKUP_MONTH_ARCHIVES="$BACKUP_DIR/month-archive"
BACKUP_LIVE="$BACKUP_DIR/live"
BACKUP_LIVE_MAX=5
NOW=`date +%s`
LATEST=`ls -c $BACKUP_LIVE | tail -n1`
WORLD_SIZE=`du -s $WORLD_DIR | cut -f 1`

LIVE_CAPACITY=$(df $BACKUP_LIVE | tail -n1 | awk '{print $4}')

if [ "$LIVE_CAPACITY" -lt "$WORLD_SIZE" ];then
	echo "FATAL: Not enough space in $BACKUP_LIVE to hold $WORLD_SIZE bytes."
	echo "Please clean up at least $(($WORLD_SIZE-$LIVE_CAPACITY)) bytes."
	exit 1
fi

umask 0002
mkdir -p $BACKUP_ARCHIVES $BACKUP_MONTH_ARCHIVES $BACKUP_LIVE

echo "Saving snapshot to $BACKUP_LIVE/$NOW"
rsync -avP $WORLD_DIR $BACKUP_LIVE/$NOW --link-dest=$BACKUP_LIVE/$LATEST --exclude-from=/srv/minecraft/server/EXCLUDE
chown :minecraft-backup -R $BACKUP_LIVE/$NOW
chmod g+rwX -R $BACKUP_LIVE/$NOW
unlink $BACKUP_LIVE/latest
ln -s $BACKUP_LIVE/$NOW $BACKUP_LIVE/latest

while [ "$(ls $BACKUP_LIVE | wc -l)" -gt $BACKUP_LIVE_MAX ];do
	sleep 1
	OLDEST=`ls -c $BACKUP_LIVE | tail -n1`
	echo "Archiving $BACKUP_LIVE/$OLDEST to $BACKUP_ARCHIVES/$OLDEST.tar"
	tar --lzop -C $BACKUP_LIVE -cf $BACKUP_ARCHIVES/$OLDEST.tar $OLDEST
	touch -r $OLDEST $BACKUP_ARCHIVES/$OLDEST.tar
	echo "Uploading to AWS glacier..."
	java -Duser.home=$BACKUP_DIR -jar $BACKUP_DIR/glacier-1.0.jar upload -queue caminus-glacier-backup -topic CaminusInfrastructure caminus-backup $BACKUP_ARCHIVES/$OLDEST.tar
	if [ $? -gt 0 ];then
		echo "FATAL: Could not archive $BACKUP_ARCHIVES/$OLDEST.tar to glacier. Quitting now before we're screwed."
		exit 1
	fi
	rm -rf $BACKUP_LIVE/$OLDEST
done
cp $BACKUP_ARCHIVES/$OLDEST.tar $BACKUP_MONTH_ARCHIVES/`date +%m-%Y`.tar


s3cmd -c $BACKUP_DIR/s3cfg sync $BACKUP_ARCHIVES/ s3://caminus-backups/`hostname`/archive/ --no-progress
s3cmd -c $BACKUP_DIR/s3cfg sync $BACKUP_MONTH_ARCHIVES/ s3://caminus-backups/`hostname`/month-archive/ --no-progress

ARCHIVE_CAPACITY=`df $BACKUP_ARCHIVES | tail -n1 | awk '{print $4}'`
echo "Current World size: $WORLD_SIZE"
WORLD_COUNT=$(($ARCHIVE_CAPACITY/$WORLD_SIZE))
echo "Capacity: $WORLD_COUNT worlds."

while [ "$ARCHIVE_CAPACITY" -lt "$WORLD_SIZE" ];do
	OLDEST=`ls -c $BACKUP_ARCHIVES | tail -n 1`
	echo "Cleaning up expired archive $BACKUP_ARCHIVES/$OLDEST"
  rm $BACKUP_ARCHIVES/$OLDEST
	ARCHIVE_CAPACITY=$(df $BACKUP_ARCHIVES | tail -n1 | awk '{print $4}')
done
