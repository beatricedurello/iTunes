from model.model import Model

mymodel = Model()
mymodel.buildGraph(120)
n,e = mymodel.getGraphDetails()
print(n,e)