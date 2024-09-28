import textwrap

story = '''Pelaaja on voittanut arvonnassa Super lentolipun, jonka avulla hän voi
matkustaa Euroopan isoille lentokentille hintaan 250 € / lento 1000 km säteellä.
Sen lisäksi hän on saanut tehtäväkseen ratkaista sana-arvoitus. Sanaan kuulu
vat 7 kirjainta on piilotettu arkkuihin ympäri Euroopan isoja lentokenttiä. Arkut voi
vat sisältää myös rahaa, rosvoja tai tyhjää. Ratkaistakseen arvoituksen, pelaa
jan täytyy etsiä kirjaimia tai arvata kyseinen sana. Sanaa voi yrittää arvata vain
ja ainoastaan pelin aloituskentällä, ja arvausyrityksiä on rajallinen määrä. Pelaa
jan täytyy lentokentille matkustaessaan huomioida myös ekologisuus. Mitä
enemmän pelaaja matkustaa, sitä vähemmän pisteitä hän saa. Jos pelaajan ra
hat tai yritykset loppuvat kesken tai pisteet vähenevät nollaan, hän epäonnistuu
tehtävässään.'''


# Set column width to 80 characters
wrapper = textwrap.TextWrapper(width=80, break_long_words=False, replace_whitespace=False)
# Wrap text
word_list = wrapper.wrap(text=story)


def getStory():
    return word_list