import json
from data.utils import str_to_dict

text = '''{
    "id":"muE3VmhJhiK",
    "isCriticalMargin":false,
    "owner_id":"5b8a7686-e060-4142-859b-ca195229c002",
    "ownerExternalId":"5b8a7686-e060-4142-859b-ca195229c002",
    "ownerUsername":"ROYALxGIFTS",
    "authorized":true,
    "fiatCurrency":{
        "id":144,
        "code":"USD",
        "name":{
            "original":"US Dollar",
            "localized":"US Dollar"
        },
        "rate":{
            "usd":1,
            "btc":19295.17,
            "usdt":1,
            "eth":1416.4,
            "usdc":1
        },
        "order":9,
        "default_amount":25,
        "flag":"US"
    },
    "paymentMethod":{
        "id":319,
        "slug":"gift-cards-miscellaneous-retailers",
        "name":{
            "original":"Gift Cards (Miscellaneous  Retailers)",
            "localized":"Gift Cards (Miscellaneous  Retailers)"},
            "groupId":1,
            "descriptionShort":"Paxful makes it easy and secure for you to buy and hold cryptocurrency. Find the best offer below and buy cryptocurrency with Gift Cards (Miscellaneous  Retailers) today.",
            "warningText":""
        },
        "fiatLimitMin":"10.00",
        "fiatLimitMax":10000,
        "fiatLimitMaxOnBalance":"10000.00",
        "newBuyerMaxFiatLimit":null,
        "margin":"100.00",
        "type":"buy",
        "isBuy":true,
        "isSell":false,
        "predefinedAmount":[],
        "paymentWindowTime":60,
        "paymentMethodLabel":"40 VARIOUS BRANDS  1229",
        "paymentMethodCountry":null,
        "paxfulFee":"5.00",

        "offerTerms":"WELCOME! THIS OFFER IS FOR 40+ OF VARIOUS BRANDS (US) <br \/>\n[Last update: December 29]<br \/>\n<br \/>\nLooking for some food &amp; restaurants gift cards? Check out our offer: NaEonu4fGpb (ID)<br \/>\n20+ brands available!<br \/>\n<br \/>\n1. L.L.Bean | paxful.com\/offer\/1n8KgvmatMX<br \/>\n2. Cabela&#039;s\/Bass Pro | paxful.com\/offer\/HUFwZNigVfm<br \/>\n3. Williams-Sonoma\/Pottery Barn | paxful.com\/offer\/6BKkxtKqyDt<br \/>\n4. Boscov&#039;s |paxful.com\/offer\/Uq5q3WiEdba<br \/>\n5. Fashion Nova | paxful.com\/offer\/v9BynJ31TeP<br \/>\n6. Madewell| paxful.com\/offer\/mRv5qNQiWBN<br \/>\n7. Wayfair | paxful.com\/offer\/Z5MYQfg3PUv<br \/>\n8. Brook Brothers | paxful.com\/offer\/uXt6UtGR44f<br \/>\n9. Vans | paxful.com\/offer\/jw4bb7i5S5i<br \/>\n10. Verizon | paxful.com\/offer\/yubJ6fyMDdw<br \/>\n11. Dick&#039;s Sporting Goods | paxful.com\/offer\/bC4NJ4WJ8w9<br \/>\n12. Carter&#039;s | paxful.com\/offer\/raTQ5VsucnF<br \/>\n*An inactive offer means that at the moment all cards are sold.<br \/>\n<br \/>\nIn current offer we sell the following brands:<br \/>\n1. Alamo Drafthouse Cinema<br \/>\n2. Fandango<br \/>\n3. Galaxy Theatres<br \/>\n4. Mandarin Oriental Hotel Group<br \/>\n5. Maurices<br \/>\n6. Tumi<br \/>\n7. Top Golf<br \/>\n8. Spa Week - Spa &amp; Wellness<br \/>\n9.  Regal Cinemas<br \/>\n10. Motherhood<br \/>\n<br \/>\nPlease choose the brand you need and make an order. Some brands may already be sold.<br \/>\n<br \/>\nWE OFFER BULK PRICE FOR SOME BRANDS!<br \/>\n<br \/>\nI. IMPORTANT INFORMATION:<br \/>\n1. Warranty period (usage time): 5 days <br \/>\n2. Region restriction: US only<br \/>\n3. Denominations: different values (from $10 to $500)<br \/>\n<br \/>\nII. OFFER&#039;S TERMS:<br \/>\n1. We check each card for the correct balance and validity before sending. Sometimes it may take some time. Please wait patiently;<br \/>\n2. Before purchasing, you must make sure that the gift cards will work in your country\/on your account. We are not responsible for any problems on your side;<br \/>\n3. If for any reason you are unable to use received gift cards, we will only be able to cancel the trade after we sell them to someone else. In other cases, we have the right not to cancel it;<br \/>\n4. You must use your gift cards within the specified warranty period. We cannot guarantee that they will be valid for a longer time if you decide to store them.<br \/>\n<br \/>\nBY OPENING A TRADE YOU AGREE TO THESE TERMS!<br \/>\n===<br \/>\n\u00a9 ROYALxGIFTS",

        "noCoins":false,
        "location":{
            "id":null,
            "countryId":null,
            "countryIso":"US",
            "countryName":"USA",
            "cityName":null,
            "subdivisionName":null,
            "prettyName":""
        },
        "fiatPricePerCrypto":"38614.320000",
        "isCashInPerson":false,
        "isCashInMail":false,
        "isGiftCard":true,
        "isGold":false,
        "showOnlyTrustedUser":false,
        "bond":{
            "isRequired":false
        },
        "requireVerifiedId":false,
        "requireMinPastTrades":null,
        "isPubliclyVisible":true,
        "requireOfferCurrencyMatchBuyerCountry":false,
        "releaseTime":14,

        "originalData":"eyJtYXJnaW4iOiIxMDAuMDAiLCJvZmZlcl90eXBlIjoxLCJwYXltZW50X21ldGhvZF9pZCI6MzE5LCJwYXltZW50X3dpbmRvdyI6NjAsImZpYXRfY3VycmVuY3lfaWQiOjE0NCwib2ZmZXJfdGVybXMiOiJXRUxDT01FISBUSElTIE9GRkVSIElTIEZPUiA0MCsgT0YgVkFSSU9VUyBCUkFORFMgKFVTKSBcbltMYXN0IHVwZGF0ZTogRGVjZW1iZXIgMjldXG5cbkxvb2tpbmcgZm9yIHNvbWUgZm9vZCAmIHJlc3RhdXJhbnRzIGdpZnQgY2FyZHM\/IENoZWNrIG91dCBvdXIgb2ZmZXI6IE5hRW9udTRmR3BiIChJRClcbjIwKyBicmFuZHMgYXZhaWxhYmxlIVxuXG4xLiBMLkwuQmVhbiB8IHBheGZ1bC5jb21cL29mZmVyXC8xbjhLZ3ZtYXRNWFxuMi4gQ2FiZWxhJ3NcL0Jhc3MgUHJvIHwgcGF4ZnVsLmNvbVwvb2ZmZXJcL0hVRndaTmlnVmZtXG4zLiBXaWxsaWFtcy1Tb25vbWFcL1BvdHRlcnkgQmFybiB8IHBheGZ1bC5jb21cL29mZmVyXC82QktreHRLcXlEdFxuNC4gQm9zY292J3MgfHBheGZ1bC5jb21cL29mZmVyXC9VcTVxM1dpRWRiYVxuNS4gRmFzaGlvbiBOb3ZhIHwgcGF4ZnVsLmNvbVwvb2ZmZXJcL3Y5QnluSjMxVGVQXG42LiBNYWRld2VsbHwgcGF4ZnVsLmNvbVwvb2ZmZXJcL21SdjVxTlFpV0JOXG43LiBXYXlmYWlyIHwgcGF4ZnVsLmNvbVwvb2ZmZXJcL1o1TVlRZmczUFV2XG44LiBCcm9vayBCcm90aGVycyB8IHBheGZ1bC5jb21cL29mZmVyXC91WHQ2VXRHUjQ0ZlxuOS4gVmFucyB8IHBheGZ1bC5jb21cL29mZmVyXC9qdzRiYjdpNVM1aVxuMTAuIFZlcml6b24gfCBwYXhmdWwuY29tXC9vZmZlclwveXViSjZmeU1EZHdcbjExLiBEaWNrJ3MgU3BvcnRpbmcgR29vZHMgfCBwYXhmdWwuY29tXC9vZmZlclwvYkM0Tko0V0o4dzlcbjEyLiBDYXJ0ZXIncyB8IHBheGZ1bC5jb21cL29mZmVyXC9yYVRRNVZzdWNuRlxuKkFuIGluYWN0aXZlIG9mZmVyIG1lYW5zIHRoYXQgYXQgdGhlIG1vbWVudCBhbGwgY2FyZHMgYXJlIHNvbGQuXG5cbkluIGN1cnJlbnQgb2ZmZXIgd2Ugc2VsbCB0aGUgZm9sbG93aW5nIGJyYW5kczpcbjEuIEFsYW1vIERyYWZ0aG91c2UgQ2luZW1hXG4yLiBGYW5kYW5nb1xuMy4gR2FsYXh5IFRoZWF0cmVzXG40LiBNYW5kYXJpbiBPcmllbnRhbCBIb3RlbCBHcm91cFxuNS4gTWF1cmljZXNcbjYuIFR1bWlcbjcuIFRvcCBHb2xmXG44LiBTcGEgV2VlayAtIFNwYSAmIFdlbGxuZXNzXG45LiAgUmVnYWwgQ2luZW1hc1xuMTAuIE1vdGhlcmhvb2RcblxuUGxlYXNlIGNob29zZSB0aGUgYnJhbmQgeW91IG5lZWQgYW5kIG1ha2UgYW4gb3JkZXIuIFNvbWUgYnJhbmRzIG1heSBhbHJlYWR5IGJlIHNvbGQuXG5cbldFIE9GRkVSIEJVTEsgUFJJQ0UgRk9SIFNPTUUgQlJBTkRTIVxuXG5JLiBJTVBPUlRBTlQgSU5GT1JNQVRJT046XG4xLiBXYXJyYW50eSBwZXJpb2QgKHVzYWdlIHRpbWUpOiA1IGRheXMgXG4yLiBSZWdpb24gcmVzdHJpY3Rpb246IFVTIG9ubHlcbjMuIERlbm9taW5hdGlvbnM6IGRpZmZlcmVudCB2YWx1ZXMgKGZyb20gJDEwIHRvICQ1MDApXG5cbklJLiBPRkZFUidTIFRFUk1TOlxuMS4gV2UgY2hlY2sgZWFjaCBjYXJkIGZvciB0aGUgY29ycmVjdCBiYWxhbmNlIGFuZCB2YWxpZGl0eSBiZWZvcmUgc2VuZGluZy4gU29tZXRpbWVzIGl0IG1heSB0YWtlIHNvbWUgdGltZS4gUGxlYXNlIHdhaXQgcGF0aWVudGx5O1xuMi4gQmVmb3JlIHB1cmNoYXNpbmcsIHlvdSBtdXN0IG1ha2Ugc3VyZSB0aGF0IHRoZSBnaWZ0IGNhcmRzIHdpbGwgd29yayBpbiB5b3VyIGNvdW50cnlcL29uIHlvdXIgYWNjb3VudC4gV2UgYXJlIG5vdCByZXNwb25zaWJsZSBmb3IgYW55IHByb2JsZW1zIG9uIHlvdXIgc2lkZTtcbjMuIElmIGZvciBhbnkgcmVhc29uIHlvdSBhcmUgdW5hYmxlIHRvIHVzZSByZWNlaXZlZCBnaWZ0IGNhcmRzLCB3ZSB3aWxsIG9ubHkgYmUgYWJsZSB0byBjYW5jZWwgdGhlIHRyYWRlIGFmdGVyIHdlIHNlbGwgdGhlbSB0byBzb21lb25lIGVsc2UuIEluIG90aGVyIGNhc2VzLCB3ZSBoYXZlIHRoZSByaWdodCBub3QgdG8gY2FuY2VsIGl0O1xuNC4gWW91IG11c3QgdXNlIHlvdXIgZ2lmdCBjYXJkcyB3aXRoaW4gdGhlIHNwZWNpZmllZCB3YXJyYW50eSBwZXJpb2QuIFdlIGNhbm5vdCBndWFyYW50ZWUgdGhhdCB0aGV5IHdpbGwgYmUgdmFsaWQgZm9yIGEgbG9uZ2VyIHRpbWUgaWYgeW91IGRlY2lkZSB0byBzdG9yZSB0aGVtLlxuXG5CWSBPUEVOSU5HIEEgVFJBREUgWU9VIEFHUkVFIFRPIFRIRVNFIFRFUk1TIVxuPT09XG5cdTAwYTkgUk9ZQUx4R0lGVFMiLCJ0cmFkZV9kZXRhaWxzIjoiSGVsbG8gJiB0aGFuayB5b3UgZm9yIHlvdXIgdHJhZGUhIFBsZWFzZSBsZXQgdXMga25vdyB3aGljaCBicmFuZCB5b3UgYXJlIGxvb2tpbmcgZm9yLlxuXG5Mb29raW5nIGZvciBzb21lIGZvb2QgJiByZXN0YXVyYW50cyBnaWZ0IGNhcmRzPyBDaGVjayBvdXQgb3VyIG9mZmVyOiBOYUVvbnU0ZkdwYiAoSUQpXG4yMCsgYnJhbmRzIGF2YWlsYWJsZSFcblxuV2UgYWxzbyBzZWxsIHRoZSBmb2xsb3dpbmcgYnJhbmRzIGluIHNlcGFyYXRlIG9mZmVycyBbQlJBTkQgXHUyMDE0IExJTktdOlxuMS4gTC5MLkJlYW4gfCBwYXhmdWwuY29tXC9vZmZlclwvMW44S2d2bWF0TVhcbjIuIENhYmVsYSdzXC9CYXNzIFBybyB8IHBheGZ1bC5jb21cL29mZmVyXC9IVUZ3Wk5pZ1ZmbVxuMy4gV2lsbGlhbXMtU29ub21hXC9Qb3R0ZXJ5IEJhcm4gfCBwYXhmdWwuY29tXC9vZmZlclwvNkJLa3h0S3F5RHRcbjQuIEJvc2NvdidzIHxwYXhmdWwuY29tXC9vZmZlclwvVXE1cTNXaUVkYmFcbjUuIEZhc2hpb24gTm92YSB8IHBheGZ1bC5jb21cL29mZmVyXC92OUJ5bkozMVRlUFxuNi4gTWFkZXdlbGx8IHBheGZ1bC5jb21cL29mZmVyXC9tUnY1cU5RaVdCTlxuNy4gV2F5ZmFpciB8IHBheGZ1bC5jb21cL29mZmVyXC9aNU1ZUWZnM1BVdlxuOC4gQnJvb2sgQnJvdGhlcnMgfCBwYXhmdWwuY29tXC9vZmZlclwvdVh0NlV0R1I0NGZcbjkuIFZhbnMgfCBwYXhmdWwuY29tXC9vZmZlclwvanc0YmI3aTVTNWlcbjEwLiBWZXJpem9uIHwgcGF4ZnVsLmNvbVwvb2ZmZXJcL3l1Yko2ZnlNRGR3XG4xMS4gRGljaydzIFNwb3J0aW5nIEdvb2RzIHwgcGF4ZnVsLmNvbVwvb2ZmZXJcL2JDNE5KNFdKOHc5XG4xMi4gQ2FydGVyJ3MgfCBwYXhmdWwuY29tXC9vZmZlclwvcmFUUTVWc3VjbkZcbipBbiBpbmFjdGl2ZSBvZmZlciBtZWFucyB0aGF0IGF0IHRoZSBtb21lbnQgYWxsIGNhcmRzIGFyZSBzb2xkLlxuXG5JbiBjdXJyZW50IG9mZmVyIHdlIHNlbGwgdGhlIGZvbGxvd2luZyBicmFuZHM6XG4xLiBBbGFtbyBEcmFmdGhvdXNlIENpbmVtYVxuMi4gRmFuZGFuZ29cbjMuIEdhbGF4eSBUaGVhdHJlc1xuNC4gTWFuZGFyaW4gT3JpZW50YWwgSG90ZWwgR3JvdXBcbjUuIE1hdXJpY2VzXG42LiBUdW1pXG43LiBUb3AgR29sZlxuOC4gU3BhIFdlZWsgLSBTcGEgJiBXZWxsbmVzc1xuOS4gIFJlZ2FsIENpbmVtYXNcbjEwLiBNb3RoZXJob29kXG5cbldFIE9GRkVSIEJVTEsgUFJJQ0UgRk9SIFNPTUUgQlJBTkRTIVxuXG5JLiBJTlNUUlVDVElPTlM6XG4xLiBNYWtlIHN1cmUgdGhhdCBpdCB3aWxsIHdvcmsgb24geW91ciBhY2NvdW50XC9pbiB5b3VyIGNvdW50cnk7XG4yLiBJbmZvcm0gdXMgd2hlbiB5b3UgYXJlIHJlYWR5IHRvIHJlY2VpdmUgeW91ciBnaWZ0IGNhcmRzO1xuMy4gUmVkZWVtIHlvdXIgZ2lmdCBjYXJkcyB3aXRoaW4gdGhlIHNwZWNpZmllZCB3YXJyYW50eSBwZXJpb2QuXG5cbklJLiBJTVBPUlRBTlQgSU5GT1JNQVRJT046XG4xLiBXYXJyYW50eSBwZXJpb2QgKHVzYWdlIHRpbWUpOiA1IGRheXMgXG4yLiBSZWdpb24gcmVzdHJpY3Rpb246IFVTIG9ubHlcbjMuIERlbm9taW5hdGlvbnM6IGRpZmZlcmVudCB2YWx1ZXMgKGZyb20gJDEwIHRvICQ1MDApXG5cblBMRUFTRSBSRUFEIFRIRSBPRkZFUidTIFRFUk1TIEJFRk9SRSBDT05USU5VSU5HIFRISVMgVFJBREUhIiwic2hvd19vbmx5X3RydXN0ZWRfdXNlciI6ZmFsc2UsInNob3dfbGltaXRfbWF4X2NvaW5zIjpmYWxzZSwicmVxdWlyZV9taW5fcGFzdF90cmFkZXMiOm51bGwsInByaWNlX2RhdGFzb3VyY2Vfa2V5IjpudWxsLCJwcmljZV9kYXRhcG9pbnRfa2V5IjpudWxsLCJyZXF1aXJlX3ZlcmlmaWVkX2lkIjpmYWxzZSwiYmxvY2tfYW5vbnltaXplcl91c2VycyI6ZmFsc2UsInRhZ3MiOlsiZS1naWZ0LWNhcmQiXSwiZmlhdF91c2RfcHJpY2VfcGVyX2NyeXB0byI6IjM4NjE0LjMyMDAwMCIsImxvY2F0aW9uX2lkIjpudWxsLCJwYXltZW50X21ldGhvZF9sYWJlbCI6IjQwIFZBUklPVVMgQlJBTkRTIC0gMTItMjkifQ==",

        "isBlocked":false,
        "timezone":"Europe\/Helsinki",
        "dutyHours":[
            {
                "day":1,
                "active":1,
                "start_time":"00:00","end_time":"00:00"},{"day":2,"active":1,"start_time":"00:00","end_time":"00:00"},{"day":3,"active":1,"start_time":"00:00","end_time":"00:00"},{"day":4,"active":1,"start_time":"00:00","end_time":"00:00"},{"day":5,"active":1,"start_time":"00:00","end_time":"00:00"},{"day":6,"active":1,"start_time":"00:00","end_time":"00:00"},{"day":7,"active":1,"start_time":"00:00","end_time":"00:00"}],"releaseTimeMedian":14,"releaseTimeMedianHumanize":" 14 min","isOnline":true,"availableIn":"2 hours","cryptoCurrencyId":1,"cryptoCurrencyName":"Bitcoin","defaultFlowType":"default","active":true,"requireFullNameVisibility":false,"isOfferTermsActual":true,"bankNameList":null,"isVerifiedMMNumberRequired":false}'''
try:
    print(str_to_dict(text))
except Exception as _ex:
    print(_ex)
# print(json.dumps(str_to_dict(text), indent=4))