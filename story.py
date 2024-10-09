import textwrap

story = '''Pelaaja on voittanut arvonnassa Super lentolipun, jonka avulla hän voi matkustaa Euroopan isoille lentokentille hintaan 250 € / lento. Sen lisäksi hän on saanut tehtäväkseen ratkaista sana-arvoitus. Sanaan kuuluvat 7 kirjainta on piilotettu arkkuihin ympäri Euroopan isoja lentokenttiä. Arkut voivat sisältää myös rahaa, rosvoja tai tyhjää. Ratkaistakseen arvoituksen, pelaajan täytyy etsiä kirjaimia tai arvata kyseinen sana. Sanaa voi yrittää arvata vain ja ainoastaan pelin aloituskentällä, ja arvausyrityksiä on rajallinen määrä. Pelaajan täytyy lentokentille matkustaessaan huomioida myös ekologisuus. Mitä enemmän pelaaja matkustaa, sitä vähemmän pisteitä hän saa. Jos pelaajan rahat tai yritykset loppuvat kesken tai pisteet vähenevät nollaan, hän epäonnistuu tehtävässään.'''



wrapper = textwrap.TextWrapper(width=100, break_long_words=False, replace_whitespace=False)
word_list = wrapper.wrap(text=story)


def getStory():
    return word_list
