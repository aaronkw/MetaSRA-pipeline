from one_vs_rest_classifier_same_features import OneVsRestClassifier
from ontology_graph import MappableOntologyGraph, Term, Synonym
from sets import Set
import json,dill,sklearn,sys,numpy

# run with python2 conda environment
f=open("/mnt/home/yliu/projects/MetaSRA-pipeline/map_sra_to_ontology/predict_sample_type/sample_type_classifier.dill", "rb")
x=dill.load(f)          #OneVsRestClassifier

x1=x.cvcl_og.id_to_term['CVCL:8U43']
x2=x.cvcl_og.id_to_term['CVCL:9W42']
 
def toJson(obj):
    try:
       cls = obj.__class__.__name__
       #print("---{} ---{}".format(obj, cls))
       s   = json.dumps(obj)
       return s
    except TypeError as err:
       if hasattr(obj, '__dict__'):
          return json.dumps({'type': cls, 'value': toJson(obj.__dict__)})
       elif isinstance(obj, numpy.int32):
          return json.dumps({'type': cls, 'value': str(obj)})
       elif isinstance(obj, (Set, tuple, numpy.ndarray)):
          v = toJson(list(obj))
          s = json.dumps({'type': cls, 'value': v})
          return s
       elif isinstance(obj, list):
          lst = map(toJson, obj)
          return '[{}]'.format(', '.join(lst))
       elif isinstance(obj, dict):
          lst = map(lambda x: '{}:{}'.format(toJson(x[0]), toJson(x[1])), obj.items())
          return '{' + ', '.join(lst) + '}'
       else:
          print("XXXXXXXXXXXXXXXXXXXXX should not be here XXXXXXXXXXXXXXXX")
          print("\t{} {}".format(cls, obj))
       #if isinstance(obj,(OneVsRestClassifier,MappableOntologyGraph,Term,Synonym,sklearn.linear_model.logistic.LogisticRegression)):
       #   return toJson(obj.__dict__)
       #elif isinstance(obj, Set):
       #   return toJson({'sets.Set': list(obj)})
       #elif isinstance(obj, tuple):
       #   return toJson({'tuple': list(obj)})
       #elif isinstance(obj, numpy.ndarray):
       #   return toJson({'numpy.ndarray': list(obj)})
       #elif isinstance(obj, numpy.int32):
       #   return toJson({'numpy.int32': str(obj)})
       #elif isinstance(obj, list):
       #   lst = map(toJson, obj)
       #   return '[{}]'.format(', '.join(lst))
       #elif isinstance(obj, dict):
       #   lst = map(lambda x: '{}:{}'.format(toJson(x[0]), toJson(x[1])), obj.items())
       #   return '{' + ', '.join(lst) + '}'
       #else:
       #   print("{}".format(obj.__class__))
       #   return json.dumps(obj)
       
j1= toJson(x)
with open("/mnt/home/yliu/c.json", "w") as f:
   json.dump(j1, f1)

def toMappableOntologyGraph(d)
    oo = toObj(d['value'])
    a1 = oo.pop('mappable_term_ids')
    new_o = MappableOntologyGraph(**oo)
    new_o.mappable_term_ids = a1
    return new_o

LogRegAttr=Set(['penalty', 'dual', 'tol', 'C', 'fit_intercept', 'intercept_scaling', 'class_weight', 'random_state', 'solver', 'max_iter', 'multi_class', 'verbose', 'warm_start', 'n_jobs', 'l1_ratio'])
def toLogisticRegression (d):
    oo = toObj(d['value'])
    print(oo)
    a1 = oo.pop('classes_')
    a2 = oo.pop('n_iter_')
    a3 = oo.pop('coef_')
    a4 = oo.pop('intercept_')
    print(Set(oo.keys()).difference(LogRegAttr))
    new_o = sklearn.linear_model.logistic.LogisticRegression(**oo)
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
       return map(toObj, d)
    elif isinstance(d, dict):
       if 'type' not in d:
          new_d = {}
          for a, v in d.items():
              new_d[a] = toObj(v)
          return new_d
       else:
          if d[u'type'] == numpy.int32.__name__:
             return numpy.int32(d[u'value'])
          elif d[u'type'] == Set.__name__:
             return Set(toObj(d['value']))  
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
          elif d['type'] == sklearn.linear_model.logistic.LogisticRegression.__name__:
             return toLogisticRegression(d)
          elif d['type'] == OneVsRestClassifier.__name__:
             return toOneVsRestClassifier(d)
          else:
             print("Type {} not dealt with\n\t{}".format(d[u'type'], dir(d['value'])))
             raw_input("Press Enter to continue...")
             return toObj(d[u'value'])
    else:
       return d  

def readObj():
    with open("/mnt/home/yliu/c.json", "r") as f:
        d2 = json.load(f2)
    o1 = toObj(d2)

#def dirmore(instance):
#    visible = dir(instance)
#    visible += [a for a in set(dir(type)).difference(visible)
#                if hasattr(instance, a)]
#    return sorted(visible)
