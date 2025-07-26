dofile("data/lib/rarity_system.lua")

function onEquip(player, item, slot)
  local mult = getItemRarityMultiplier(item)
  item:setAttribute(ITEM_ATTRIBUTE_ATTACK, item:getAttack() * mult)
  item:setAttribute(ITEM_ATTRIBUTE_DEFENSE, item:getDefense() * mult)
  item:setAttribute(ITEM_ATTRIBUTE_ARMOR, item:getArmor() * mult)
  return true
end
