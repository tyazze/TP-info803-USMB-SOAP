from spyne import Application, rpc, ServiceBase, \
    Integer, Unicode
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


# nom : autonomie, tempsCharge
carList = {
    "SmartFor2":[160, 1],
    "Zoe":[400, 3],
    "SmartFor4":[155, 1],
    "C0":[150, 2],
    "iOn":[150, 1]
    }

class CorsService(ServiceBase):
    origin = '*'

def _on_method_return_object(ctx):
    ctx.transport.resp_headers['Access-Control-Allow-Origin'] = \
                                              ctx.descriptor.service_class.origin

CorsService.event_manager.add_listener('method_return_object',
                                                        _on_method_return_object)

class VeicleListService(CorsService):
    @rpc(Unicode, _returns=Iterable(Unicode))
    def autonomy(ctx, name):
        res = carList[name][0]
        yield u'%s' % res


    @rpc(Unicode, _returns=Iterable(Unicode))
    def chargeTime(ctx, name):
        res = carList[name][1] 
        yield u'%s' % res

application = Application([VeicleListService], 'spyne.examples.hello.soap',
                            in_protocol=Soap11(validator='lxml'),
                            out_protocol=Soap11())
wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()
