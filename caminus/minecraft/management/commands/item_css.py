from django.core.management.base import BaseCommand
from minecraft.items import ITEMS

class Command(BaseCommand):
  help = 'Generate item CSS'

  def handle(self, *args, **options):
    items = [
      [ 'LEATHER_HELMET', 'CHAINMAIL_HELMET', 'IRON_HELMET', 'DIAMOND_HELMET', 'GOLD_HELMET', 'FLINT_AND_STEEL', 'FLINT', 'COAL'],
      [ 'LEATHER_CHESTPLATE', 'CHAINMAIL_CHESTPLATE', 'IRON_CHESTPLATE', 'DIAMOND_CHESTPLATE', 'GOLD_CHESTPLATE', 'BOW', 'CLAY_BRICK', 'IRON_INGOT', 'FEATHER', 'WHEAT', 'PAINTING', 'SUGAR_CANE', 'BONE', 'CAKE', 'SLIME_BALL'],
      [ 'LEATHER_LEGGINGS', 'CHAINMAIL_LEGGINGS', 'IRON_LEGGINGS', 'DIAMOND_LEGGINGS', 'GOLD_LEGGINGS', 'ARROW', '', 'GOLD_INGOT', 'SULPHUR', 'BREAD', 'SIGN', 'WOODEN_DOOR', 'IRON_DOOR', 'BED', 'FIREBALL'],
      [ 'LEATHER_BOOTS', ],
      [ 'WOOD_SWORD', ],
      [ 'WOOD_SPADE', ],
      [ 'WOOD_PICKAXE', ],
      [ 'WOOD_AXE', ],
      [ 'WOOD_HOE', ],
    ]

    terrain = [
      [ '', 'STONE', 'DIRT', 'GRASS', 'WOOD', 'DOUBLE_STEP', '', 'BRICK', 'TNT', '', '', 'WEB', 'RED_ROSE', 'YELLOW_FLOWER', '', 'SAPLING'],
      [ 'COBBLESTONE', 'BEDROCK', 'SAND', 'GRAVEL', 'LOG', '', 'IRON_BLOCK', 'GOLD_BLOCK', 'DIAMOND_BLOCK', 'EMERALD_BLOCK', '', '', 'RED_MUSHROOM', 'BROWN_MUSHROOM', ],
      ['GOLD_ORE', 'IRON_ORE', 'COAL_ORE', 'BOOKSHELF', 'MOSSY_COBBLESTONE', 'OBSIDIAN', '', 'LONG_GRASS', '', '', '', '', 'FURNACE', '', 'DISPENSER'],
      ['SPONGE', 'GLASS', 'DIAMOND_ORE', 'REDSTONE_ORE', 'LEAVES', 'SMOOTH_BRICK', 'DEAD_BUSH', '', '', '', '', 'WORKBENCH', '', '', ''],
      ['WOOL', 'MOB_SPAWNER', 'SNOW', 'ICE', '', '', 'CACTUS', '', '', 'SUGAR_CANE_BLOCK', 'JUKEBOX', '', 'WATER_LILY', 'MYCEL', '', ''],
      ['TORCH', '', '', 'LADDER', 'TRAP_DOOR', 'IRON_FENCE', ],
      ['LEVER', '', '', 'REDSTONE_TORCH_ON', '', '', '', 'NETHERRACK', 'SOUL_SAND', 'GLOWSTONE', 'PISTON_STICKY_BASE', 'PISTON_BASE',],
    ]

    print "/* Automatically generated via item_css django command */"
    for dataset,img in ((items, 'items.png'), (terrain, 'terrain.png')):
      y = 0
      for row in dataset:
        x = 0
        for column in row:
          found = False
          if column == "":
            continue
          for i in ITEMS:
            if i['name'] == column:
              print ".inventory-item-%d { /* %s */"%(i['id'], i['name'])
              print "  background-position: %d %d !important;"%(x, y)
              print "  background-image: url(images/%s) !important"%(img)
              print "}"
              found = True
              break
          if not found:
            raise Exception, "Unknown item name: %s"%(column)
          x -= 64
        y -= 64
