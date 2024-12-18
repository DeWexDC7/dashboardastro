from . import db

class Datos(db.Model):
    __tablename__ = 'datos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    direccion = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Datos {self.nombre}>'
    
    
class Tipo_Inventario(db.Model):
    __tablename__ = 'tipo_inventario'
    
    id_tipo_inv = db.Column(db.Integer, primary_key=True)
    nombre_inv = db.Column(db.String(50), nullable=False)
    descripcion_inv = db.Column(db.Text, nullable=False)
    
    tipos_dato = db.relationship(
        'Tipo_Dato', 
        back_populates="tipo_inventario", 
        foreign_keys='Tipo_Dato.fk_tipo_inv'
    )
    
    registros_inventario = db.relationship(
        'Registro_Inventario',
        back_populates='tipo_inventario',
        foreign_keys='Registro_Inventario.fk_tipo_inv'
    )
    
    def __repr__(self):
        return f'<Datos {self.nombre_inv}>'
    
    
class Tipo_Dato(db.Model):
    __tablename__ = 'tipo_dato'
    
    id_tipo_dato = db.Column(db.Integer, primary_key=True)
    tipo_dato = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    fk_tipo_inv = db.Column(db.Integer, db.ForeignKey('tipo_inventario.id_tipo_inv'), primary_key=True)
    
    tipo_inventario = db.relationship(
        'Tipo_Inventario',
        back_populates="tipos_dato",
        foreign_keys=[fk_tipo_inv]
    )
    
    registros_inventario_campos = db.relationship(
        'Registro_Inventario_Campos',
        back_populates='tipo_dato_padre',
        foreign_keys='Registro_Inventario_Campos.fk_tipo_dato'
    )
    
    
    def __repr__(self):
        return f'<Datos {self.nombre}>'
 
class Roles(db.Model):
    __tablename__ = 'roles'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(50), nullable=False)
    
    usuarios = db.relationship('Usuario', back_populates="rol")
    
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_user = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    fk_rol = db.Column(db.Integer, db.ForeignKey('roles.id_rol'))
    fk_dpto = db.Column(db.Integer, db.ForeignKey('departamento.id_dtp'))
    fk_jefe = db.Column(db.Integer, db.ForeignKey('usuario.id_user'))
    
    rol = db.relationship('Roles', back_populates="usuarios")
    jefe = db.relationship(
        'Usuario', 
        remote_side=[id_user], 
        primaryjoin="Usuario.fk_jefe == Usuario.id_user",
        backref='subordinados', 
        uselist=False
    )
    departamento = db.relationship('Departamento', back_populates="usuario", foreign_keys=[fk_dpto])
    departamento_jefe = db.relationship('Departamento', back_populates="jefe", foreign_keys='Departamento.fk_jefe')
    registro_inventario = db.relationship('Registro_Inventario', back_populates='ing_responsable', foreign_keys='Registro_Inventario.fk_ing_responsable')
 
class Departamento(db.Model):
    __tablename__ = 'departamento'
    id_dtp = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fk_departamento_sup = db.Column(db.Integer, db.ForeignKey('departamento.id_dtp'), nullable=True)
    fk_jefe = db.Column(db.Integer, db.ForeignKey('usuario.id_user'), nullable=False)
    #fk_segundo_mando = db.Column(db.Integer, db.ForeignKey('usuario.id_user'), nullable=False)
    
    usuario = db.relationship('Usuario', back_populates="departamento", foreign_keys="Usuario.fk_dpto")
    jefe = db.relationship('Usuario', back_populates="departamento_jefe", foreign_keys='Departamento.fk_jefe')
    departamento_sup = db.relationship('Departamento', remote_side=[id_dtp], backref='departamentos', uselist=False)
    registros_inventario = db.relationship('Registro_Inventario', back_populates="departamento", foreign_keys='Registro_Inventario.fk_departamento')
    
    def __repr__(self):
        return f"<Departamento(id_dtp={self.id_dtp}, nombre='{self.nombre}', fk_departamento_sup={self.fk_departamento_sup})>"
    
class Registro_Inventario(db.Model):
    __tablename__ = 'registro_inventario'
    id_registro = db.Column(db.Integer, primary_key=True)
    fk_departamento = db.Column(db.Integer, db.ForeignKey('departamento.id_dtp'), nullable=False)
    fk_ing_responsable = db.Column(db.Integer, db.ForeignKey('usuario.id_user'), nullable=False)
    fk_tipo_inv = db.Column(db.Integer, db.ForeignKey('tipo_inventario.id_tipo_inv'), nullable=False)
    estado_activo = db.Column(db.Boolean, nullable=False)
    
    departamento = db.relationship('Departamento', back_populates="registros_inventario", foreign_keys=[fk_departamento])
    ing_responsable = db.relationship('Usuario', back_populates='registro_inventario', foreign_keys=[fk_ing_responsable])
    registros_inventario_campos = db.relationship('Registro_Inventario_Campos', back_populates='registro_inventario_padre', foreign_keys='Registro_Inventario_Campos.fk_registro_inventario')
    tipo_inventario = db.relationship(
        'Tipo_Inventario', 
        back_populates='registros_inventario', 
        foreign_keys=[fk_tipo_inv]
    )

class Registro_Inventario_Campos(db.Model):
    __tablename__ = 'registro_inventario_campos'
    id_reg_cps = db.Column(db.Integer, primary_key=True)
    valor_numero = db.Column(db.Integer, nullable=True)
    valor_texto = db.Column(db.String(100), nullable=True)
    valor_booleano = db.Column(db.Boolean, nullable=True)
    valor_datetime = db.Column(db.DateTime, nullable=True)
    estado_activo = db.Column(db.Boolean, nullable=False)
    #valor_catalogo = db.Column(db.Integer, db.ForeignKey('usuario.id_user'), nullable=False)
    #fk_inventario_campo = db.Column(db.Integer, db.ForeignKey('inventario_campo.id_inv_cp'), nullable=False)
    fk_tipo_dato = db.Column(db.Integer, db.ForeignKey('tipo_dato.id_tipo_dato'), nullable=False) 
    fk_registro_inventario = db.Column(db.Integer, db.ForeignKey('registro_inventario.id_registro'), nullable=False) 
    
    registro_inventario_padre = db.relationship(
        'Registro_Inventario', 
        back_populates="registros_inventario_campos",
        foreign_keys=[fk_registro_inventario]
    )
    
    tipo_dato_padre = db.relationship(
        'Tipo_Dato',
        back_populates='registros_inventario_campos',
        foreign_keys=[fk_tipo_dato]
    )
    
   #inventario_campo = db.relationship('Inventario_Campo', back_populates="registros_inventario_campos", foreign_keys=[fk_inventario_campo])