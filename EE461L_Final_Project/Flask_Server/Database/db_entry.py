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
 
    def create(self, data_set):
        return self.client.create(data_set)
  
    def update(self, selector, data_set):
        return self.client.update(selector, data_set)
  
    def delete(self, selector):
        return self.client.delete(selector)
