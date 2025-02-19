from app.models.drink import Drink


async def convert(
        source_drink: Drink,
        source_ml: int,
        target_drink: Drink
):
    source_alc = (source_ml / 100) * source_drink.average_strength
    target_ml = (source_alc / target_drink.average_strength) * 100
    return round(target_ml, 1)
