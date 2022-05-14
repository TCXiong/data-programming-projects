# project: p3
# submitter: txiong53@wisc.edu
# partner: none
# hours: 12

import pandas as pd
import time
import requests

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        # 1. clear out visited set
        # 2. start recursive search by calling dfs_visit
        self.visited.clear()
        self.order.clear()
        self.dfs_visit(node)

    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        # 2. mark node as visited by adding it to the set
        # 3. add this node to the end of self.order
        # 4. get list of node's children with this: self.go(node)
        # 5. in a loop, call dfs_visit on each of the children
        if node in self.visited:
            return 
        self.visited.add(node)
        self.order.append(node)
        Children = self.go(node)
        
        for child in Children:
            self.dfs_visit(child)
            
    def bfs_search(self, node):
        todo = []
        todo.append(node)
        self.visited.add(node)            
        while len(todo)>0:
            cur = todo.pop(0)
            self.order.append(cur)
            children = self.go(cur)
            for child in children:
                if not child in self.visited:
                    todo.append(child)
                    self.visited.add(child)
        
                     
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def go(self, node):
        children = []
        # TODO: use `self.df` to determine what children the node has and append them        
        for node, has_edge in self.df.loc[node].items():
            if has_edge==1:
                children.append(node)
        return children
    
      
    
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
        #store the children
        self.Children = list()
        #store the value of node
        self.valueList = list()
                
    def go(self, filePath):      
        count = 0
        with open(f"file_nodes/{filePath}") as f:
            for line in f:
                for word in line.split():
                    if count == 0:
                        self.valueList.append(word)
                    if count > 0:
                        self.Children = word.split(",")
                    count+=1
        return self.Children
               
    def message(self):
        msg = ""
        for i in self.valueList:
            msg += i
        return msg
        
  


        
class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.tableList = []   
        
    def go(self, node):
        children = []
        self.driver.get(node)
        links = self.driver.find_elements(by="tag name", value="a")
        for link in links:
            child_url = link.get_attribute("href")
            children.append(child_url)     
        tables = pd.read_html(self.driver.page_source)
        self.tableList.append(tables[0])
        self.visited.add(node)
        return children

    def table(self):
        return pd.concat(self.tableList, ignore_index=True)



        
        
        

def reveal_secrets(driver, url, travellog):
    password = ""
    res = travellog["clue"].tolist()
    for i in res:
        password+=str(i)

    driver.get(url)
    inputBox = driver.find_element(value="password")
    button = driver.find_element(value="attempt-button")
    inputBox.send_keys(password)
    button.click()
    
    btn2 = driver.find_element(value="securityBtn")
    btn2.click()
    time.sleep(2)
    img = driver.find_element(value="image")
    img_url = img.get_attribute("src")
    r = requests.get(img_url, allow_redirects=True)
   
    with open("Current_Location.jpg", 'wb') as f: 
        f.write(r.content)
    
    location = driver.find_element(value="location")
    
    return location.text    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
 