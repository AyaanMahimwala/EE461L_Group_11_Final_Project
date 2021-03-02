class DataSet(object):
    """
    Abstract data base entry representing a data set with api calls as follows
    """
    def __init__(self, adapter=None):
        self.client = adapter()

    def find_all(self, selector):
        return self.client.find_all(selector)
 
    def find(self, selector):
        return self.client.find(selector)
 
    def create(self, set):
        return self.client.create(set)
  
    def update(self, selector, set):
        return self.client.update(selector, set)
  
    def delete(self, selector):
        return self.client.delete(selector)
