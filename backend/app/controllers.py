import inspect
from .models import Datos
from .models import Tipo_Inventario, Tipo_Dato, Usuario, Registro_Inventario, Registro_Inventario_Campos
from sqlalchemy.orm import subqueryload, relationship, state, collections

from . import db

def get_all_users():
    users = Datos.query.all()
    return [{'id': user.id, 'nombre': user.nombre, 'direccion': user.direccion, 'telefono': user.telefono} for user in users]

def get_user_by_id(user_id):
    user = Datos.query.get_or_404(user_id)
    return {'id': user.id, 'nombre': user.nombre, 'direccion': user.direccion, 'telefono': user.telefono}

def create_user(data):
    new_user = Datos(nombre=data['nombre'], direccion=data['direccion'], telefono=data['telefono'])
    db.session.add(new_user)
    db.session.commit()
    return {'id': new_user.id, 'nombre': new_user.nombre, 'direccion': new_user.direccion, 'telefono': new_user.telefono}

def update_user(user_id, data):
    user = Datos.query.get_or_404(user_id)
    user.nombre = data['nombre']
    user.direccion = data['direccion']
    user.telefono = data['telefono']
    db.session.commit()
    return {'id': user.id, 'nombre': user.nombre, 'direccion': user.direccion, 'telefono': user.telefono}

def delete_user(user_id):
    user = Datos.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

def get_all_tipo_inventario():
    
    resultados = Tipo_Inventario.query.options(subqueryload(Tipo_Inventario.tipos_dato)).all()
    
    tipos_inventario_arr = []
    
    for inventario in resultados:
        ti_var_dict = {}
        
        for attr_name, attr_value in inventario.__dict__.items():
            # el attr_value puede ser de un tipo de dato propio de dbModel. Con esto se lo evita
            if isinstance(attr_value, state.InstanceState):
                continue
            
            if not isinstance(attr_value, collections.InstrumentedList):
                ti_var_dict[attr_name] = attr_value
            
            # Algunos atributos de la clase puede ser una lista a otro modelo,
            # aqui se iteran los elementos de la lista
            if isinstance(attr_value, collections.InstrumentedList):
                arr_elements = []
                var_element_dict = {}
                
                for element in attr_value:
                    for column in element.__table__.columns:
                        var_element_dict[column.name] = element.__getattribute__(column.name)   

                    arr_elements.append(var_element_dict)
                    var_element_dict = {}
                
                ti_var_dict[attr_name] = arr_elements
        
        tipos_inventario_arr.append(ti_var_dict)
        
    return tipos_inventario_arr

def get_tipo_inventario_by_id(id_tipo_inv):
    tipo_inventario = Tipo_Inventario.query.get_or_404(id_tipo_inv)
    
    #for tipo_inventario in  arr_tipo_inventario:
    tipo_inventario_dict = {
        'id_tipo_inv': tipo_inventario.id_tipo_inv,
        'nombre_inv': tipo_inventario.nombre_inv,
        'descripcion_inv': tipo_inventario.descripcion_inv
    }
    

    if tipo_inventario.registros_inventario:
        arr_element = []
        
        for element in tipo_inventario.registros_inventario:
            
            if element.estado_activo: 
                id_registro = element.id_registro
                arr_element.append(get_registro_inventario_by_id(id_registro))
        
        tipo_inventario_dict['registros_inventario'] = arr_element
            
    return tipo_inventario_dict
        
    
    
def get_all_tipo_dato():
    resultados = Tipo_Dato.query.options(subqueryload(Tipo_Dato.tipo_inventario)).all()

    arr_response = []

    for tipo_dato in resultados:
        dict_tipo_dato = {
            "tipo_dato": tipo_dato.tipo_dato,
            "id_tipo_dato": tipo_dato.id_tipo_dato,
            "nombre": tipo_dato.nombre
        }
        
        arr_response.append(dict_tipo_dato)
    
    return arr_response 
    
    
def get_usuario_by_id(id_user):
    user = Usuario.query.get_or_404(id_user)
    
    response_dict = {
        'id': user.id_user,
        'nombre': user.nombre
    }
    
    if user.departamento:
        dpto_nombre = user.departamento.nombre
        response_dict['dpto'] = dpto_nombre
    
    if user.jefe:
        jefe_nombre = user.jefe.nombre
        response_dict['jefe'] = jefe_nombre
    
    return response_dict



def get_registro_inventario_by_id(id_registro):
    registro_inventario = Registro_Inventario.query.get_or_404(id_registro)
    
    if not registro_inventario.estado_activo:
        return None
    
    response_dict = {
        'id_registro': registro_inventario.id_registro,
        'fk_ing_responsable': registro_inventario.fk_ing_responsable,
        'fk_departamento': registro_inventario.fk_departamento,
        'fk_tipo_inv': registro_inventario.fk_tipo_inv,
        'estado_activo': registro_inventario.estado_activo
    }
    
    if registro_inventario.departamento:
        response_dict['dpt_nombre'] = registro_inventario.departamento.nombre
    
    if registro_inventario.ing_responsable:
        response_dict['ing_responsable_nombre'] = registro_inventario.ing_responsable.nombre
        
        
    if registro_inventario.registros_inventario_campos:
        arr_response = []
    
        for element in registro_inventario.registros_inventario_campos:
            element_dict = get_registro_inventario_campo_by_id(element.id_reg_cps)
            arr_response.append(element_dict)
            
        response_dict['registro_inventario_campos'] = arr_response
        
    return response_dict


def get_registro_inventario_campo_by_id(id_reg_cps):
    registro_inventario_campo = Registro_Inventario_Campos.query.get_or_404(id_reg_cps)
    
    
    response_dict = {
        'id_reg_cps': registro_inventario_campo.id_reg_cps,
        'estado_activo': registro_inventario_campo.estado_activo
    }

    if registro_inventario_campo.tipo_dato_padre:
        response_dict['fk_tipo_dato'] = registro_inventario_campo.tipo_dato_padre.id_tipo_dato
        response_dict['tipo_dato'] = registro_inventario_campo.tipo_dato_padre.tipo_dato
        response_dict['tipo_dato_nombre'] = registro_inventario_campo.tipo_dato_padre.nombre
    
    if response_dict['tipo_dato'] == 'varchar':
        response_dict['valor'] = registro_inventario_campo.valor_texto
    
    if response_dict['tipo_dato'] == 'boolean':
        response_dict['valor'] = registro_inventario_campo.valor_booleano
    
    return response_dict

def get_all_registro_inventario_campos():
    reg_inv_cps = Registro_Inventario_Campos.query.all()
    
    arr_response = []
    
    for element in reg_inv_cps:
        element_dict = {
            'id_reg_cps': element.id_reg_cps,
            'valor_texto': element.valor_texto,
            'fk_registro_inventario': element.fk_registro_inventario
        }
        
        if element.inventario_campo:
            element_dict['fk_tipo_inv'] = element.inventario_campo.fk_tipo_inv
        
        arr_response.append(element_dict)
    
    return arr_response

def create_registro_inventario(data):
    
    new_registro_inventario = Registro_Inventario(
        fk_departamento=2,
        fk_ing_responsable=7,
        fk_tipo_inv=data['fk_tipo_inv'],
    )
    
    reg_inv_dict = {
        'fk_departamento': new_registro_inventario.fk_departamento,
        'fk_ing_responsable': new_registro_inventario.fk_ing_responsable,
        'fk_tipo_inv': new_registro_inventario.fk_tipo_inv
    }
    
    db.session.add(new_registro_inventario)
    db.session.commit()
    
    arr_reg_inv_cps_dict = []
    arr_reg_inv_cps = data['registro_inventario_campos']
    id_registro = new_registro_inventario.id_registro
    
    if len(arr_reg_inv_cps) > 0:
        for element in arr_reg_inv_cps:
            reg_inv_cp_dict = create_registro_inventario_campo(element, id_registro)
            arr_reg_inv_cps_dict.append(reg_inv_cp_dict)
    
    reg_inv_dict['registro_inventario_campos'] = arr_reg_inv_cps_dict
    
    return reg_inv_dict

def update_registro_inventario(id_registro, data):
    
    reg_inv = Registro_Inventario.query.get_or_404(id_registro)
    
    reg_inv.fk_departamento=2
    reg_inv.fk_ing_responsable=7
    #reg_inv.fk_tipo_inv=data['fk_tipo_inv']
    
    reg_inv_dict = {
        'id_registro': reg_inv.id_registro,
        'fk_departamento': reg_inv.fk_departamento,
        'fk_ing_responsable': reg_inv.fk_ing_responsable,
        #'fk_tipo_inv': reg_inv.fk_tipo_inv
    }
    
    db.session.commit()

    arr_reg_inv_cps_dict = []
    arr_reg_inv_cps = data['registro_inventario_campos']
    id_registro = reg_inv.id_registro
    
    if len(arr_reg_inv_cps) > 0:
        for element in arr_reg_inv_cps:
            reg_inv_cp_dict = update_registro_inventario_campos(element['id_reg_cps'], element)
            arr_reg_inv_cps_dict.append(reg_inv_cp_dict)
    
    reg_inv_dict['registro_inventario_campos'] = arr_reg_inv_cps_dict
    
    
    return reg_inv_dict

def delete_registro_inventario(id_registro):
    reg_inv = Registro_Inventario.query.get_or_404(id_registro)
    reg_inv.estado_activo = False
    
    db.session.commit()
    
    if reg_inv.registros_inventario_campos:
        for element in reg_inv.registros_inventario_campos:
            delete_registro_inventario_campos(element.id_reg_cps)
    
    return '', 204
    

def create_registro_inventario_campo(data, fk_registro_inventario):
    
    new_reg_inv_cps = Registro_Inventario_Campos(
        fk_tipo_dato=data['fk_tipo_dato'],
        fk_registro_inventario=fk_registro_inventario
    )
    
    tipos_datos = {
        "varchar": "valor_texto",
        "boolean": "valor_booleano"
    }
    
    new_reg_inv_cps.__setattr__(
        tipos_datos[data['tipo_dato']],
        data['valor']
    )
    
    db.session.add(new_reg_inv_cps)
    db.session.commit()
    
    reg_inv_cps_dict = {
        
        'fk_tipo_dato': new_reg_inv_cps.fk_tipo_dato,
        'fk_registro_inventario': new_reg_inv_cps.fk_registro_inventario,
        'valor': data['valor']
    }
    
    return reg_inv_cps_dict

def update_registro_inventario_campos(id_reg_cps, data):
    reg_inv_cps = Registro_Inventario_Campos.query.get_or_404(id_reg_cps)
    
    tipos_datos = {
        "varchar": "valor_texto",
        "boolean": "valor_booleano"
    }
    
    reg_inv_cps.__setattr__(
        tipos_datos[data['tipo_dato']],
        data['valor']
    )
    
    reg_inv_cps_dict = {
        'fk_tipo_dato': reg_inv_cps.fk_tipo_dato,
        'fk_registro_inventario': reg_inv_cps.fk_registro_inventario,
        'valor': data['valor'],
        'id_reg_cps': reg_inv_cps.id_reg_cps
    }
    
    db.session.commit()
    return reg_inv_cps_dict

def delete_registro_inventario_campos(id_reg_cps):
    reg_inv_cps = Registro_Inventario_Campos.query.get_or_404(id_reg_cps)
    reg_inv_cps.estado_activo = False
    db.session.commit()
    return '', 204