
from bs4 import BeautifulSoup
import urllib
list_of_edges=[]
list_of_nodes=[]
url = 'http://forum.hse.ru/newforum/index.php?t=thread&frm_id=125&S=113870092c010050c608f900a805de56&start='
page_number = ['0', '40', '80', '120']
for i in range(4):
    page = urllib.urlopen(url + page_number[i])
    soup = BeautifulSoup(page.read())
    for each_a in soup.findAll('a', {'class':'big'}):
        thread = each_a.get('href')
        thread = "http://forum.hse.ru/newforum/" + thread
        thread = thread.replace('msg', 'tree')
        page = urllib.urlopen(thread)
        soup = BeautifulSoup(page.read(), fromEncoding="cp1251")
        users = []
        previous_padding = -1;
        for each_td in soup.findAll('td', {'class':'Gentext nw wa vt'}):
            current_padding = each_td['style']
            current_padding = current_padding.replace('px', '');
            current_padding = current_padding.replace('padding-left: ', '');
            current_padding = int(current_padding)
            current_user = str(each_td.findAll('a')[1].string.encode('utf-8'))
            print current_user
            if current_user not in list_of_nodes:
                list_of_nodes.append(current_user)
            flag = 1
            while current_padding <= previous_padding:
                flag = 0
                user1 = users[-1]
                users.pop(-1)
                user2 = users[-1]
                temp_list = []
                temp_list.append(user1)
                temp_list.append(user2)
                list_of_edges.append(temp_list)
                previous_padding = previous_padding - 15
            if flag:
                previous_padding = current_padding
            users.append(current_user)
        
        while len(users) > 1:
            user1 = users[-1]
            users.pop(-1)
            user2 = users[-1]
            temp_list = []
            temp_list.append(user1)
            temp_list.append(user2)
            list_of_edges.append(temp_list)
output = open('graph_replies.gdf', 'w')
output.write('nodedef>name VARCHAR,label VARCHAR,color VARCHAR' + '\n')
list_of_nodes.sort()
r = 0;
g = 0;
b = 100;
for each_node in list_of_nodes:
    rgb = str(r) + ',' + str(g) + ',' + str(b)
    r = r + 4;
    if r >= 255:
        r = 255
        g = g + 4
    if g >= 255:
        g = 255
        r = r - 8
    output.write(each_node + ',')
    output.write(each_node + ',')
    output.write("'" + rgb + "'\n")
output.write('edgedef>node1 VARCHAR,node2 VARCHAR' + '\n')
for each_edge in list_of_edges:
    output.write(each_edge[0] + ',')
    output.write(each_edge[1] + '\n')
output.close()



