#coding: utf8

from app import app
from flask import render_template
from urllib2 import Request, urlopen, URLError
from bs4 import BeautifulSoup
import logging
import sys

#--------------- LOGGER ----------------
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s -  %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

LOGGER=logging.getLogger("MyInstapaper")

@app.route('/')
def index():
    url = "https://sivers.org/blog"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:48.0) Gecko/20100101 Firefox/48.0"
    data_filename = "./app/static/data.txt"

    articles = []
    #On ouvre le blog de Derek :
    try:
        request = Request(url, headers={'User-Agent': user_agent})
        response=urlopen(request)
        soup = BeautifulSoup(response.read(), 'html.parser')

        #On récupère les urls et les titres des articles présents
        for tag in soup.findAll('a'):
            articles.append((unicode(tag['href']), unicode(tag.string)))

        del articles[0]
        LOGGER.info("Found " + str(len(articles)) + " articles")

        #print "=========================="
        #print "Articles from website :"
        #print articles
        #print "=========================="

        #On regarde dans le fichier data quels sont les articles que l'on a pas encore
        m_file = open(data_filename, "r")
        last_article=m_file.readline();
        m_file.close()

        if(last_article == ""):
            m_file=open(data_filename, "w")
            for article in articles:
                LOGGER.debug("Writing article : " + unicode(article[1]))
                m_file.write(unicode(article[0]).encode('utf8') + unicode(" | ").encode('utf8') + unicode(article[1]).encode('utf8') + "\n")
            m_file.close()
            LOGGER.info("No last article found, write all found articles into data.txt file")

        else:
            index=0
            for i in articles:
                if unicode(i[0]).encode('utf8') in last_article:
                    LOGGER.info("Found last article : " + last_article)
                    break
                index+=1

            if(index == 0):
                return render_template('index.html', url=url)
            else:
                new_articles = []
                for i in range(0, index):
                    print articles[i]
                    new_articles.append(articles[i])
                LOGGER.debug("Found " + str(len(new_articles)) + " new articles")
                return render_template('index.html', url=url, articles=new_articles)

        return "Hello, World!"

    except URLError, e:
        print "Error while communicating with remote server : "
        print e


    #On les affiche dans une liste que l'on présente à l'utilisateur

    #L'utilisateur choisit les liens qu'il veut ajouter à Instapaper

    #Parcours des liens et ajout à Instapaper
