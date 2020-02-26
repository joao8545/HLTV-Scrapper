import requests
from bs4 import BeautifulSoup as Soup
from datetime import datetime
import csv
from contextlib import suppress
"""
TODO




"""

erros=0

def myRequest(url,erro):
    global erros
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',}
    while True:
            try:
                r=requests.get(url,headers=headers)
            except Exception:
                print("\a\n\n\n\n",erro,"\n\n\n\n\a")
                erros+=1
            else:
                if r.status_code != 200:
                    erros+=1
                break
            
    return r

startTime = datetime.now()

#def scrape():
#    global erros

for jj in range(0,94):
    offset=jj*100
    pagina="https://www.hltv.org/results?offset="+str(offset)+"&team=9215&team=6667&team=4411&team=5752&team=5973&team=6665&team=4608&team=4494&team=6290&team=6211&team=7801&team=6673&team=4991&team=7533&team=7532&team=4869&team=5310&team=5005&team=5995&team=6619&team=8668&team=7606&team=8113"
    r=myRequest(pagina,"erro na pagina de resultados "+str(jj))
     
       
    soup=Soup(r.text,"html.parser")
    r.close()
    """
    '''
    pegar o link de cada resultado fazer uma lista
    abrir cada link
    pegar os nomes e ids das equipes, mapa, hora, resultado, line up

    '''
    """
    urls=[]
    links=[]
    for link in soup.find("div",{'class':"results-all"}).find_all('a'):
        cont=link.get('href')
        if cont is not None:
            if "/matches/" in cont:
                links.append(cont)
                urls.append("https://www.hltv.org"+cont)
                #print(cont)
    for index in range(0,len(urls)):
        
        #print("Partida número: ",index," da página: ",jj)
        r=myRequest(urls[index],"erro na pagina de partida"+str(index))
        
        soup=Soup(r.text,"html.parser")
        r.close()
        lineup=soup.find("div", {"class":"lineups"})

        teams=[]
        for team in lineup.find_all("img",{'class':'logo'}):
            teams.append(team.get('title'))

        players={}
        aux1=0
        

        for tr in lineup.find_all('tr'):
            aux1=aux1+1
            play=[]
            for player in tr.find_all("div", {"class":"text-ellipsis"}):
                    play.append(player.text)
            if len(play)==0:
                    continue
            while len(play)<5:
                play.append("vazio")
            players[aux1]=play
           

        equipe={}
        for i in range(0,len(teams)):
            equipe[teams[i]]=players[2*(i+1)]

        
        maps=[]
        for mapa in soup.find('div', {'class':"flexbox-column"}).find_all('div',{'class':'mapname'}):
            if mapa.text=="Default":
                continue
            maps.append(mapa.text)

        results=[]
        for result in soup.find_all('div', {'class':"results"}):
                results.append(result.findAll('div',{'class':'results-team-score'})[0].text+':'+result.findAll('div',{'class':'results-team-score'})[1].text)
        resultados={}
        finais=[]
        for i in range(0,len(results)):
            resultados[maps[i]]=results[i]
            final=results[i].split(":")

            try:
                if int(final[0])>int(final[1]):
                    final="A"
                elif int(final[0])<int(final[1]):
                    final="B"
                else:
                    final="E"
            except ValueError:
                final="N"
            finais.append(final)

        data=soup.find('div', {'class':"timeAndEvent"}).find('div', {'class':"date"}).text
        hora=soup.find('div', {'class':"timeAndEvent"}).find('div', {'class':"time"}).text
        evento=soup.find('div', {'class':"event text-ellipsis"}).text
        
##        print("os times foram:%s, %s"%(teams[0],teams[1]))
##        print("a configuração foi")
##        print(equipe)
##        print("os mapas foram")
##        print(maps)
##        print("os resultados foram")
##        print(resultados)
##        print("aconteceu em",data,"as",hora)
##        print("gastei um total de ")
##        print(datetime.now() - startTime)

        
        
        with open("dbteste.csv","a")as csvfile:
            pass
            csv_writer=csv.writer(csvfile,delimiter=';')
            if (jj==0 and index==0):
                row="Time A,,JogadorA1,,JogadorA2,,JogadorA3,,JogadorA4,,JogadorA5,,Time B,,JogadorB1,,JogadorB2,,JogadorB3,,JogadorB4,,JogadorB5,,Mapa,,ResultadoA,,ResultadoB,,Hora,,Data,,Evento"
                csv_writer.writerow(row.split(',,'))
            for i in range(0,len(results)):
                row=teams[0]+',,'+',,'.join(equipe[teams[0]])+',,'+teams[1]+',,'+',,'.join(equipe[teams[1]])+',,'+maps[i]+',,'+",,".join(resultados[maps[i]].split(":"))+',,'+finais[i]+',,'+hora+',,'+data+',,'+evento
                try:
                    csv_writer.writerow(row.split(',,'))
                except Exception:
                    print("nao escreveu")
                    erros+=1
                else:
                    pass
                    print(teams[0],equipe[teams[0]],teams[1],equipe[teams[1]],maps[i],resultados[maps[i]],hora,data,evento)

            print("o resultado dessa partida ficou pronto ",datetime.now() - startTime," depois de começar o programa")
            print("total de erros ",erros)
    print("O resultado da pagina ",jj," ficou pronto ",datetime.now() - startTime," depois de começar o programa")
    print("total de erros ",erros)




#scrape()
