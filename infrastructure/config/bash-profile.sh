if hostname | grep dev > /dev/null; then
  HOSTCOLOR='\[\e[1;32m\]'
else
  HOSTCOLOR='\[\e[1;31m\]'
fi
[ "$PS1" = "\\s-\\v\\\$ " ] && PS1="[\u@$HOSTCOLOR\H\[\e[0m\] \W]\\$ "
