from data.models import *

offers = Offer.objects.filter(subcategory__id=91).order_by('-margin').select_related('offer_detail')

display_offers = [offers[0]]
min = offers[0].offer_detail.fiat_amount_range_min
max = offers[0].offer_detail.fiat_amount_range_max
pr_amount = offers[0].offer_detail.predefined_amount \
    if type(offers[0].offer_detail.predefined_amount) == list else []
for idx in range(1, len(offers)):
    if offers[idx].offer_info() != offers[idx-1].offer_info():
        if offers[idx].offer_detail.predefined_amount != 'null':
            if set(offers[idx].offer_detail.predefined_amount) - set(pr_amount):
                pr_amount.extend(offers[idx].offer_detail.predefined_amount)
                display_offers.append(offers[idx])
        elif offers[idx].offer_detail.fiat_amount_range_min < min:
            min = offers[idx].offer_detail.fiat_amount_range_min
            display_offers.append(offers[idx])
        elif offers[idx].offer_detail.fiat_amount_range_max > max:
            max = offers[idx].offer_detail.fiat_amount_range_max
            display_offers.append(offers[idx])
        