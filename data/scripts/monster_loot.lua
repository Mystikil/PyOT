dofile("data/lib/rarity_system.lua")

function onKill(creature, target)
  if not target:isMonster() then return true end

  local corpse = target:getCorpse()
  if not corpse then return true end

  local container = corpse:getContainer()
  if not container then return true end

  for i = 0, container:getSize() - 1 do
    local item = container:getItem(i)
    if item then
      local rarity = assignRandomRarity()
      local info = RARITY_CONFIG[rarity]
      local serial = os.time() .. math.random(1000, 9999)
      local rarityName = formatRarityPrefix(rarity)

      item:setAttribute(ITEM_ATTRIBUTE_CUSTOM, rarity)
      item:setAttribute(ITEM_ATTRIBUTE_SERIAL, serial)
-- item:setAttribute(ITEM_ATTRIBUTE_NAME, rarityName .. " " .. item:getName())  -- Removed to prevent OTClient opcode error

      local dropPos = container:getPosition()
      if info.effect then
        dropPos:sendMagicEffect(info.effect)
      end

      if rarity >= BROADCAST_RARITY_THRESHOLD then
        Game.broadcastMessage(string.format("[LOOT] %s dropped a %s!", creature:getName(), item:getName()), MESSAGE_STATUS_WARNING)
      end
    end
  end

  return true
end
