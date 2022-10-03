from one_vs_rest_classifier_same_features import OneVsRestClassifier
from ontology_graph import MappableOntologyGraph, Term, Synonym
import json,dill,sklearn,sys,numpy


#x1=x.cvcl_og.id_to_term['CVCL:8U43']
#x2=x.cvcl_og.id_to_term['CVCL:9W42']
 
with open("/mnt/home/yliu/c.json", "r") as f:
    d2 = json.load(f)

def toMappableOntologyGraph(d):
    oo = toObj(d['value'])
    a1 = oo.pop('mappable_term_ids')
    new_o = MappableOntologyGraph(**oo)
    new_o.mappable_term_ids = a1
    return new_o

LogRegAttr=set(['penalty', 'dual', 'tol', 'C', 'fit_intercept', 'intercept_scaling', 'class_weight', 'random_state', 'solver', 'max_iter', 'multi_class', 'verbose', 'warm_start', 'n_jobs', 'l1_ratio'])
def toLogisticRegression (d):
    oo = toObj(d['value'])
    print(oo)
    a1 = oo.pop('classes_')
    a2 = oo.pop('n_iter_')
    a3 = oo.pop('coef_')
    a4 = oo.pop('intercept_')
    print(set(oo.keys()).difference(LogRegAttr))
    new_o = sklearn.linear_model.LogisticRegression(**oo)
    new_o.classes_, new_o.n_iter_, new_o.coef_, new_o.intercept_ = a1, a2, a3, a4
    return new_o

def toOneVsRestClassifier(d):
    oo = toObj(d['value'])
    print(oo)
    sav = {}
    for attr in ['feature_cutoff', 'filt_features', 'class_to_classifier']:
        sav[attr] = oo.pop(attr)
    new_o = OneVsRestClassifier(**oo)
    new_o.feature_cutoff = sav['feature_cutoff']
    new_o.filt_features = sav['filt_features']
    new_o.class_to_classifier = sav['class_to_classifier']
    return new_o

def toObj (s):
    try:
       d = json.loads(s)
    except (ValueError,TypeError) as err:
       d = s
    if isinstance(d, list):
       return list(map(toObj, d))
    elif isinstance(d, dict):
       if 'type' not in d:
          new_d = {}
          for a, v in d.items():
              new_d[a] = toObj(v)
          return new_d
       else:
          if d[u'type'] == numpy.int32.__name__:
             return numpy.int32(d[u'value'])
          elif d[u'type'] == 'Set':
             return set(toObj(d['value']))  
          elif d[u'type'] == tuple.__name__:
             return tuple(toObj(d[u'value']))
          elif d[u'type'] == numpy.ndarray.__name__:
             oo = toObj(d['value'])
             return numpy.array(oo)
          elif d['type'] == Synonym.__name__:
             return Synonym(**toObj(d['value']))
          elif d['type'] == Term.__name__:
             return Term(**toObj(d['value']))
          elif d['type'] == MappableOntologyGraph.__name__:
             return toMappableOntologyGraph(d)
          elif d['type'] == sklearn.linear_model.LogisticRegression.__name__:
             return toLogisticRegression(d)
          elif d['type'] == OneVsRestClassifier.__name__:
             return toOneVsRestClassifier(d)
          else:
             print("Type {} not dealt with\n\t{}".format(d[u'type'], dir(d['value'])))
             raw_input("Press Enter to continue...")
             return toObj(d[u'value'])
    else:
       return d  

o=toObj(d2)
with open("/mnt/home/yliu/c.dill","wb") as f:
    dill.dump(o,f)

def readObj():
    with open("/mnt/home/yliu/projects/MetaSRA-pipeline/map_sra_to_ontology/predict_sample_type/c.dill","rb") as f:
        o1 = dill.load(f)
    return o1
#3lass User(object)u
#    def __init__(self, name, username):
#        self.name = name
#        self.username = username

#f2= open("/mnt/home/yliu/c.json", "rb")
#d2 = json.load(f2)
#d3 = json.loads(d2)
#x2 = OneVsRestClassifier(d3['classif_type'], d3['ngram_vec_scaffold'], d3['term_vec_scaffold'], d3['cvcl_og'])

    
#u = User(**j)

#def dirmore(instance):
#    visible = dir(instance)
#    visible += [a for a in set(dir(type)).difference(visible)
#                if hasattr(instance, a)]
#    return sorted(visible)
