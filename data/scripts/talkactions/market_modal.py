from game.market import getMarket
from game.item import Item

@register("talkaction", "/market")
def open_market(creature, text, **k):
    """Open the custom modal based market browser."""
    if creature.client.version < 944:
        creature.openMarket()
    else:
        creature.market = getMarket(0)
        creature.marketOpen = True

    show_main_menu(creature)
    return False


def show_main_menu(player):
    buttons = [(0, "View Offers"), (1, "Create Offer"), (2, "Exit")]
    player.sendModalWindow("Market", "Select an action", buttons,
                           callback=lambda b, c: handle_main_menu(player, b))


def handle_main_menu(player, button):
    if button == 0:
        browse_items(player, action="view")
    elif button == 1:
        player.modal_tmp = {}
        select_offer_type(player)


def browse_items(player, action="view"):
    items = list(player.market.getItems())
    choices = []
    mapping = {}
    for idx, (itemId, _) in enumerate(items[:250]):
        choices.append((idx, Item(itemId).name))
        mapping[idx] = itemId
    player.modal_map = mapping
    player.sendModalWindow("Items", "Choose an item", [(0, "Ok"), (1, "Cancel")],
                           choices, callback=lambda b, ch: handle_item_select(player, b, ch, action))


def handle_item_select(player, button, choice, action):
    if button != 0:
        return
    itemId = player.modal_map.get(choice)
    if itemId is None:
        return
    if action == "view":
        show_offers(player, itemId)
    else:
        player.modal_tmp["item"] = itemId
        select_quantity(player)


def show_offers(player, itemId):
    sells = player.market.getSaleOffers(itemId, player.data["id"])
    lines = [f"{o.amount}x {Item(o.itemId).name} for {o.price} gp" for o in sells]
    message = "\n".join(lines) if lines else "No offers."
    player.sendModalWindow("Offers", message, [(0, "Close")])


def select_offer_type(player):
    buttons = [(0, "Buy"), (1, "Sell"), (2, "Cancel")]
    player.sendModalWindow("Offer Type", "Choose type", buttons,
                           callback=lambda b, c: handle_offer_type(player, b))


def handle_offer_type(player, button):
    if button in (0, 1):
        player.modal_tmp["type"] = 0 if button == 0 else 1
        browse_items(player, action="create")


def select_quantity(player):
    choices = [(0, "1"), (1, "5"), (2, "10"), (3, "100")]
    mapping = {0: 1, 1: 5, 2: 10, 3: 100}
    player.modal_map = mapping
    player.sendModalWindow("Quantity", "Select amount", [(0, "Ok")], choices,
                           callback=lambda b, ch: handle_quantity(player, b, ch))


def handle_quantity(player, button, choice):
    if button != 0:
        return
    amt = player.modal_map.get(choice, 1)
    player.modal_tmp["amount"] = amt
    select_price(player)


def select_price(player):
    choices = [(0, "100"), (1, "1000"), (2, "10000")]
    mapping = {0: 100, 1: 1000, 2: 10000}
    player.modal_map = mapping
    player.sendModalWindow("Price", "Select price", [(0, "Ok")], choices,
                           callback=lambda b, ch: handle_price(player, b, ch))


def handle_price(player, button, choice):
    if button != 0:
        return
    price = player.modal_map.get(choice, 0)
    t = player.modal_tmp
    player.createMarketOffer(t["type"], t["item"], t["amount"], price)
    player.sendModalWindow("Market", "Offer created.", [(0, "Ok")])
