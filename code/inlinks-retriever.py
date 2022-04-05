import wikipediaapi
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import wikipediaapi
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)



#def print_langlinks(page):
#        langlinks = page.langlinks#aurl:
#        for k in sorted(langlinks.keys()):#ista:
#            v = langlinks[k]#
#            #print("%s: %s - %s: %s" % (k, v.language, v.title, v.fullurl))# = wikipediaapi.Wikipedia(lang)
#            langu = k
#            fullink = v.fullurl
#            return langu, fullink
#dik = {}
#print_langlinks(page_py)
import wikipediaapi
df = pd.read_csv('Table wikipedia tutta - gr_import2.csv')

#df = df.head(5)
opere = df.label
wiki_wiki = wikipediaapi.Wikipedia('it')
import time
for opera in opere:
        dik = {}
        time.sleep(5)
        wiki_wiki = wikipediaapi.Wikipedia('it')
        try:
            urlpagina = wiki_wiki.page(opera).fullurl
            print(urlpagina)
        except KeyError:
            print("nothing for", opera)
            pass

        wikipage = urlpagina.split('/wiki/')[1]
        page_py = wiki_wiki.page(wikipage)
        langlinks = page_py.langlinks
        langlinks.update({'it':page_py})

        print(langlinks)
        for k in sorted(langlinks.keys()):
            v = langlinks[k]
            try:
                urlserve = v.fullurl.split('/wiki/')[1]
            except KeyError:
                urlserve = wikipage
                continue
            wiki_wiki2 = wikipediaapi.Wikipedia(k)
            page_py2 = wiki_wiki2.page(urlserve)
            try:
                backlinks = page_py2.backlinks
            except KeyError:
                backlinks = []
                continue
            if dik.get(k) is None:
                dik.update({k:len(backlinks)})
                #dik[k] = len(backlinks)
                print(dik)
                pd.DataFrame.from_dict(dik.items()).to_csv(f"{opera}_INLINKS_4.csv")


            #listalingue.append(langlinks[k])
           # listaurl.append (langlinks[k].fullurl)
#print(listalingue,listaurl)
            #v = langlinks[k]  #ho le lingue
            # print("%s: %s - %s: %s" % (k, v.language, v.title, v.fullurl))
            #langu = k
            #urlpagina2 = v.fullurl
            #print(langu, urlpagina2)
            #wiki_wiki2 = wikipediaapi.Wikipedia(langu)
            #wikipage2 = urlpagina2.split('/wiki/')[1]
            #page_py2 = wiki_wiki2.page(wikipage2)
            #backlinks = page_py2.backlinks
            #dik[langu] = len(backlinks)
            #pd.DataFrame.from_dict(dik.items()).to_csv(f"{opera}_OK.csv")
            #fullink = v.fullurl
            #print(langu, fullink)






