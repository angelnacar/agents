

# Technical Architecture Design Document
## Prototipo de Aplicación de Gastos Personales

---

## 1. Información General del Documento

| Campo | Detalle |
|-------|---------|
| **Versión del Documento** | 1.0 |
| **Fecha de Creación** | Enero 2025 |
| **Autor** | Tech Lead |
| **Documento Base** | PRD_Prototipo_Gastos_Personales.md v1.0 |
| **Estado** | Listo para Implementación |

---

## 2. Resumen Ejecutivo

### 2.1 Propósito del Documento

Este documento define la arquitectura técnica detallada del prototipo de aplicación de gestión de gastos personales. Establece el diseño del modelo de datos, la estructura de componentes, los patrones de diseño implementados, y la estrategia de despliegue para garantizar escalabilidad, seguridad y eficiencia.

### 2.2 Decisiones Arquitecturales Clave

| Decisión | Selección | Justificación |
|----------|-----------|---------------|
| Paradigma | Programación Orientada a Objetos (POO) | Encapsulamiento de lógica de negocio, reutilización de código, fácil mantenimiento |
| Patrón de Arquitectura | Layered Architecture (3-Tier) | Separación clara de concerns: UI, Servicios, Datos |
| Almacenamiento | Estructuras en memoria con patrón Repository | Preparado para migración futura a base de datos |
| Frontend | Gradio (monolítico con backend) | Framework requerido, prototipado rápido |
| Estructura de Datos | Diccionarios y Listas en memoria | Simplicidad para prototipo, sin dependencias externas |

---

## 3. Modelo de Datos

### 3.1 Diagrama de Entidad-Relación (ER)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           MODELO DE DATOS EN MEMORIA                            │
│                              (Prototipo v1.0)                                    │
└──────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────┐         1:N         ┌─────────────────────┐
    │       USUARIO        │───────────────────────▶│       GASTO         │
    │   (Entity/User)     │                        │  (Entity/Expense)   │
    ├─────────────────────┤                        ├─────────────────────┤
    │ PK  username        │                        │ PK  id (UUID)       │
    │     password       │                        │ FK  user_id         │
    │     full_name      │                        │     description     │
    │     created_at     │                        │     amount          │
    │     updated_at     │                        │     date            │
    │     is_active      │                        │     category        │
    └─────────────────────┘                        │     created_at      │
                                                  │     updated_at      │
                                                  └─────────────────────┘
                                                           │
                                                           │ N:1
                                                           ▼
                                                  ┌─────────────────────┐
                                                  │     CATEGORÍA      │
                                                  │  (Config/Category)  │
                                                  ├─────────────────────┤
                                                  │     name            │
                                                  │     icon            │
                                                  │     keywords[]      │
                                                  │     color           │
                                                  └─────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────┐
│                            SESSION STATE                                        │
├──────────────────────────────────────────────────────────────────────────────────┤
│  current_session: Optional[User]  ────────▶ Mantiene referencia al usuario      │
│                                        activo durante la sesión de Gradio       │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Modelo Físico de Datos (En Memoria)

#### 3.2.1 Estructura de Almacenamiento

```python
# =============================================================================
# ESTRUCTURAS DE DATOS GLOBALES (EN MEMORIA)
# =============================================================================

# Base de datos de usuarios: {username: User}
users_db: Dict[str, User] = {}

# Base de datos de gastos: Lista de objetos Expense
expenses_db: List[Expense] = []

# Sesión actual del usuario (mantenida por Gradio State)
current_session: Optional[User] = None

# Sesión de gastos del usuario actual
session_expenses: List[Expense] = []
```

### 3.3 Definición de Entidades

#### 3.3.1 Entidad: User (Usuario)

```python
@dataclass
class User:
    """
    Entidad que representa un usuario del sistema.
    
    Attributes:
        username: Identificador único del usuario (PK natural)
        password: Contraseña del usuario (en prototipo sin hash)
        full_name: Nombre completo del usuario
        created_at: Fecha y hora de creación de la cuenta
        updated_at: Fecha y hora de última modificación
        is_active: Bandera que indica si el usuario está activo
    """
    username: str
    password: str
    full_name: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
    def __post_init__(self):
        """Valida los campos después de la inicialización."""
        if len(self.username) < 4:
            raise ValueError("El nombre de usuario debe tener al menos 4 caracteres")
        if len(self.password) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres")
        if len(self.full_name) < 3:
            raise ValueError("El nombre completo debe tener al menos 3 caracteres")
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
```

**Restricciones de Integridad:**
- `username`: Único, mínimo 4 caracteres, alfanumérico
- `password`: Mínimo 4 caracteres (en prototipo sin hash)
- `full_name`: Mínimo 3 caracteres

#### 3.3.2 Entidad: Expense (Gasto)

```python
@dataclass
class Expense:
    """
    Entidad que representa un gasto registrado por un usuario.
    
    Attributes:
        id: Identificador único del gasto (UUID)
        user_id: Referencia al usuario propietario (FK)
        description: Descripción textual del gasto
        amount: Monto del gasto (positivo, 2 decimales)
        date: Fecha en que se realizó el gasto
        category: Categoría asignada (manual o automática)
        created_at: Fecha y hora de creación del registro
        updated_at: Fecha y hora de última modificación
    """
    id: str
    user_id: str
    description: str
    amount: float
    date: datetime
    category: str
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """Valida los campos después de la inicialización."""
        if self.amount <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        if len(self.description) > 200:
            raise ValueError("La descripción no puede exceder 200 caracteres")
        if self.date > datetime.now():
            raise ValueError("La fecha no puede ser futura")
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
```

**Restricciones de Integridad:**
- `id`: Único, formato UUID
- `amount`: Mayor que 0, máximo 2 decimales
- `description`: Máximo 200 caracteres
- `date`: No puede ser futura
- `category`: Debe existir en la lista de categorías válidas

#### 3.3.3 Entidad: Category (Categoría)

```python
@dataclass
class Category:
    """
    Entidad que representa una categoría de gastos.
    
    Attributes:
        name: Nombre de la categoría (único)
        icon: Icono emoji asociado
        keywords: Lista de palabras clave para categorización automática
        color: Color hexadecimal para gráficos
    """
    name: str
    icon: str
    keywords: List[str]
    color: str
    
    def matches_keyword(self, text: str) -> bool:
        """Verifica si el texto contiene alguna palabra clave."""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in self.keywords)
```

**Categorías Predefinidas:**

| Categoría | Icono | Color | Palabras Clave |
|-----------|-------|-------|----------------|
| Vivienda | 🏠 | #2E86AB | alquiler, hipoteca, luz, agua, gas, internet, teléfono, mantenimiento |
| Alimentación | 🍔 | #A23B72 | comida, supermercado, restaurante, cena, almuerzo, desayuno, delivery |
| Transporte | 🚗 | #F18F01 | gasolina, taxi, uber, bus, metro, estacionamiento, peaje |
| Entretenimiento | 🎮 | #C73E1D | cine, netflix, spotify, videojuegos, teatro, museo, viaje, vacaciones |
| Compras | 🛒 | #3B1F2B | ropa, zapatos, electrónica, tablet, hogar, decoración, regalo, amazon |
| Salud | 💊 | #95C11F | médico, farmacia, medicina, dentista, seguro médico, gimnasio, fitness |
| Educación | 📚 | #7B2D8E | curso, universidad, libro, escuela, formación, certificación |
| Otros | 💰 | #6B7280 | (ninguna - fallback por defecto) |

---

## 4. Arquitectura del Sistema

### 4.1 Vista General de Capas

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           ARQUITECTURA EN CAPAS                                 │
│                          (3-Tier Layered Architecture)                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                      CAPA DE PRESENTACIÓN (UI)                          │  │
│  │                         Gradio Interface                                 │  │
│  ├───────────────────────────────────────────────────────────────────────────┤  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │  │
│  │  │   AuthUI     │  │  ExpenseUI   │  │ StatisticsUI │  │ Components  │ │  │
│  │  │  (Login/     │  │  (CRUD       │  │  (Dashboard  │  │ (Reusable   │ │  │
│  │  │   Register)  │  │   Expenses)  │  │   & Charts)  │  │  Elements)  │ │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └─────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                           │
│                                    ▼                                           │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                      CAPA DE NEGOCIO (SERVICES)                           │  │
│  │                    Lógica de Aplicación                                  │  │
│  ├───────────────────────────────────────────────────────────────────────────┤  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │  │
│  │  │ AuthService │  │ExpenseService│  │Categorization│  │Statistics   │ │  │
│  │  │             │  │              │  │   Service    │  │  Service    │ │  │
│  │  │ - register  │  │ - create     │  │              │  │             │ │  │
│  │  │ - login     │  │ - update     │  │ - categorize │  │ - get_total │ │  │
│  │  │ - logout    │  │ - delete     │  │ - get_all    │  │ - by_category│  │
│  │  │             │  │ - get_list   │  │ - get_by_name│  │ - get_average│  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └─────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                           │
│                                    ▼                                           │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                      CAPA DE DATOS (REPOSITORIES)                         │  │
│  │                    Abstracción de Persistencia                           │  │
│  ├───────────────────────────────────────────────────────────────────────────┤  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────────────┐ │  │
│  │  │UserRepository│  │ExpenseRepository│ │ CategoryRepository (Config)   │ │  │
│  │  │              │  │                │ │                              │ │  │
│  │  │ + add()      │  │ + add()        │ │ + get_all()                   │ │  │
│  │  │ + get()      │  │ + update()     │ │ + get_by_name()               │ │  │
│  │  │ + get_all()  │  │ + delete()     │ │ + find_by_keyword()           │ │  │
│  │  │ + exists()   │  │ + get_by_user()│ │                              │ │  │
│  │  │ + update()   │  │ + filter()     │ │                              │ │  │
│  │  └──────────────┘  └────────────────┘ └────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                           │
│                                    ▼                                           │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                         CAPA DE INFRAESTRUCTURA                           │  │
│  │                    Almacenamiento en Memoria                             │  │
│  ├───────────────────────────────────────────────────────────────────────────┤  │
│  │                                                                             │  │
│  │   users_db: Dict[str, User]        expenses_db: List[Expense]              │  │
│  │   ┌─────────────────────────┐      ┌─────────────────────────┐            │  │
│  │   │  "usuario1" → User     │      │  [Expense1, ...]       │            │  │
│  │   │  "usuario2" → User     │      │  ┌───────────────────┐  │            │  │
│  │   │  ...                   │      │  │ expense.id        │  │            │  │
│  │   └─────────────────────────┘      │  │ expense.user_id   │  │            │  │
│  │                                    │  │ expense.amount    │  │            │  │
│  │                                    │  │ ...               │  │            │  │
│  │                                    │  └───────────────────┘  │            │  │
│  │                                    └─────────────────────────┘            │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Flujo de Datos

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FLUJO DE DATOS                                    │
│                        Ejemplo: Registrar un Gasto                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  USUARIO                    UI (Gradio)              SERVICES              DATA │
│     │                           │                       │                   │   │
│     │  1. Ingresa datos         │                       │                   │   │
│     │  ─────────────────────────▶                       │                   │   │
│     │                           │                       │                   │   │
│     │                           │  2. Captura evento    │                   │   │
│     │                           │  click "Guardar"       │                   │   │
│     │                           │  ─────────────────────▶                   │   │
│     │                           │                       │                   │   │
│     │                           │                       │ 3. Validación     │   │
│     │                           │                       │ ───────┬──────────│   │
│     │                           │                       │        │          │   │
│     │                           │                       │ 4. ¿Válido?       │   │
│     │                           │                       │        │          │   │
│     │                           │                       │        ▼          │   │
│     │                           │                       │ 5. Categorización │   │
│     │                           │                       │    automática     │   │
│     │                           │                       │        │          │   │
│     │                           │                       │        ▼          │   │
│     │                           │                       │ 6. Crear Expense  │   │
│     │                           │                       │ ────────────────▶ │   │
│     │                           │                       │                   │   │
│     │                           │  7. Notificar éxito  │                   │   │
│     │  8. Mostrar confirmación │◀─────────────────────                   │   │
│     │  ◀────────────────────────│                       │                   │   │
│     │                           │                       │                   │   │
│     │                           │  9. Refrescar UI      │                   │   │
│     │                           │  (actualizar lista    │                   │   │
│     │                           │   y estadísticas)    │                   │   │
│     │                           │                       │                   │   │
│     ▼                           ▼                       ▼                   ▼   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Especificación de Servicios

### 5.1 AuthService (Servicio de Autenticación)

#### 5.1.1 Responsabilidades

- Gestionar el registro de nuevos usuarios
- Validar credenciales de login
- Mantener el estado de sesión del usuario
- Manejar logout

#### 5.1.2 Interfaz Pública

```python
class AuthService:
    """
    Servicio de autenticación que maneja el registro, login y logout de usuarios.
    
    Este servicio utiliza el patrón Repository para abstraer el acceso a los datos
    de usuarios, permitiendo una futura migración a base de datos sin modificar
    la lógica de negocio.
    """
    
    def __init__(self, user_repository: IUserRepository):
        """
        Constructor del servicio de autenticación.
        
        Args:
            user_repository: Repositorio de usuarios (inyección de dependencias)
        """
        self._repository = user_repository
        self._current_user: Optional[User] = None
    
    def register(
        self,
        username: str,
        password: str,
        full_name: str
    ) -> Result[User]:
        """
        Registra un nuevo usuario en el sistema.
        
        Args:
            username: Nombre de usuario único (mínimo 4 caracteres)
            password: Contraseña (mínimo 4 caracteres)
            full_name: Nombre completo (mínimo 3 caracteres)
            
        Returns:
            Result[User]: Resultado con el usuario creado o error
            
        Raises:
            ValidationError: Si los datos no cumplen las validaciones
        """
        pass
    
    def login(self, username: str, password: str) -> Result[User]:
        """
        Autentica a un usuario con sus credenciales.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            Result[User]: Resultado con el usuario autenticado o error
            
        Note:
            En el prototipo, la comparación de contraseñas es directa.
            En producción, se utilizaría hashing (bcrypt/argon2).
        """
        pass
    
    def logout(self) -> None:
        """
        Cierra la sesión del usuario actual.
        
        Limpia el usuario actual de la sesión y prepara el sistema
        para un nuevo login.
        """
        pass
    
    @property
    def current_user(self) -> Optional[User]:
        """
        Obtiene el usuario actualmente autenticado.
        
        Returns:
            Optional[User]: El usuario actual o None si no hay sesión activa
        """
        pass
    
    def is_authenticated(self) -> bool:
        """
        Verifica si hay un usuario autenticado en la sesión.
        
        Returns:
            bool: True si hay un usuario autenticado, False en caso contrario
        """
        pass
```

#### 5.1.3 Contrato (Resultado de Operaciones)

```python
@dataclass
class Result:
    """
    Tipo de resultado genérico para operaciones de servicio.
    
    Utiliza el patrón Result para manejar tanto éxitos como errores
    sin lanzar excepciones, permitiendo un flujo de control más limpio.
    """
    success: bool
    data: Any = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    
    @classmethod
    def ok(cls, data: Any = None) -> 'Result':
        """Crea un resultado exitoso."""
        return cls(success=True, data=data)
    
    @classmethod
    def fail(cls, error: str, error_code: str = None) -> 'Result':
        """Crea un resultado de error."""
        return cls(success=False, error=error, error_code=error_code)
```

---

### 5.2 ExpenseService (Servicio de Gastos)

#### 5.2.1 Responsabilidades

- Crear, leer, actualizar y eliminar gastos
- Aplicar validaciones de negocio
- Mantener integridad referencial con usuarios
- Soportar filtrado y búsqueda

#### 5.2.2 Interfaz Pública

```python
class ExpenseService:
    """
    Servicio de gestión de gastos que implementa las operaciones CRUD
    y la lógica de negocio relacionada con los gastos del usuario.
    """
    
    def __init__(
        self,
        expense_repository: IExpenseRepository,
        categorization_service: CategorizationService
    ):
        """
        Constructor del servicio de gastos.
        
        Args:
            expense_repository: Repositorio de gastos
            categorization_service: Servicio de categorización automática
        """
        self._repository = expense_repository
        self._categorization = categorization_service
    
    def create_expense(
        self,
        user_id: str,
        description: str,
        amount: float,
        date: datetime,
        category: Optional[str] = None
    ) -> Result[Expense]:
        """
        Crea un nuevo gasto para el usuario especificado.
        
        Args:
            user_id: ID del usuario propietario
            description: Descripción del gasto
            amount: Monto del gasto (debe ser mayor a 0)
            date: Fecha del gasto (no puede ser futura)
            category: Categoría manual (opcional, se asigna automáticamente si no se proporciona)
            
        Returns:
            Result[Expense]: Resultado con el gasto creado o error
        """
        pass
    
    def update_expense(
        self,
        expense_id: str,
        user_id: str,
        updates: Dict[str, Any]
    ) -> Result[Expense]:
        """
        Actualiza un gasto existente.
        
        Args:
            expense_id: ID del gasto a actualizar
            user_id: ID del usuario (para verificación de propiedad)
            updates: Diccionario con los campos a actualizar
            
        Returns:
            Result[Expense]: Resultado con el gasto actualizado o error
        """
        pass
    
    def delete_expense(
        self,
        expense_id: str,
        user_id: str
    ) -> Result[bool]:
        """
        Elimina un gasto existente.
        
        Args:
            expense_id: ID del gasto a eliminar
            user_id: ID del usuario (para verificación de propiedad)
            
        Returns:
            Result[bool]: Resultado indicando éxito o error
        """
        pass
    
    def get_expenses(
        self,
        user_id: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Expense]:
        """
        Obtiene la lista de gastos del usuario con filtros opcionales.
        
        Args:
            user_id: ID del usuario propietario
            filters: Filtros opcionales (category, date_from, date_to)
            
        Returns:
            List[Expense]: Lista de gastos que cumplen los filtros
        """
        pass
    
    def get_expense_by_id(
        self,
        expense_id: str,
        user_id: str
    ) -> Optional[Expense]:
        """
        Obtiene un gasto específico por su ID.
        
        Args:
            expense_id: ID del gasto
            user_id: ID del usuario (para verificación de propiedad)
            
        Returns:
            Optional[Expense]: El gasto encontrado o None
        """
        pass
    
    def get_user_expenses_for_period(
        self,
        user_id: str,
        year: int,
        month: int
    ) -> List[Expense]:
        """
        Obtiene todos los gastos del usuario para un período específico.
        
        Args:
            user_id: ID del usuario propietario
            year: Año del período
            month: Mes del período
            
        Returns:
            List[Expense]: Lista de gastos del período
        """
        pass
```

---

### 5.3 CategorizationService (Servicio de Categorización)

#### 5.3.1 Responsabilidades

- Mantener el catálogo de categorías disponibles
- Implementar el algoritmo de categorización automática
- Gestionar palabras clave por categoría

#### 5.3.2 Interfaz Pública

```python
class CategorizationService:
    """
    Servicio de categorización automática de gastos.
    
    Utiliza un algoritmo basado en palabras clave para clasificar
    automáticamente los gastos en categorías predefinidas.
    """
    
    # Constante para categoría por defecto cuando no hay match
    DEFAULT_CATEGORY = "Otros"
    
    def __init__(self, category_repository: ICategoryRepository):
        """
        Constructor del servicio de categorización.
        
        Args:
            category_repository: Repositorio de categorías
        """
        self._repository = category_repository
    
    def categorize(self, description: str) -> Category:
        """
        Categoriza automáticamente un gasto basado en su descripción.
        
        El algoritmo:
        1. Normaliza el texto (convierte a minúsculas)
        2. Busca coincidencias parciales de palabras clave
        3. Retorna la primera categoría con match
        4. Si no hay match, retorna la categoría "Otros"
        
        Args:
            description: Descripción del gasto a categorizar
            
        Returns:
            Category: La categoría asignada automáticamente
        """
        pass
    
    def get_all_categories(self) -> List[Category]:
        """
        Obtiene todas las categorías disponibles.
        
        Returns:
            List[Category]: Lista de todas las categorías del sistema
        """
        pass
    
    def get_category_names(self) -> List[str]:
        """
        Obtiene solo los nombres de las categorías disponibles.
        
        Returns:
            List[str]: Lista de nombres de categorías
        """
        pass
    
    def get_category_by_name(self, name: str) -> Optional[Category]:
        """
        Obtiene una categoría específica por su nombre.
        
        Args:
            name: Nombre de la categoría a buscar
            
        Returns:
            Optional[Category]: La categoría encontrada o None
        """
        pass
```

#### 5.3.3 Algoritmo de Categorización

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     ALGORITMO DE CATEGORIZACIÓN AUTOMÁTICA                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  FUNCIÓN: categorize(description: str) -> Category                             │
│                                                                                 │
│  INICIO                                                                         │
│     │                                                                           │
│     ▼                                                                           │
│  ┌─────────────────┐                                                           │
│  │ Normalizar texto│  description_clean = description.lower().strip()          │
│  └────────┬────────┘                                                           │
│           │                                                                     │
│           ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    PARA CADA categoría EN categories                    │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐ │   │
│  │  │   PARA CADA keyword EN categoría.keywords                         │ │   │
│  │  │   ┌─────────────────────────────────────────────────────────────┐ │ │   │
│  │  │   │   SI keyword.lower() ESTÁ EN description_clean             │ │ │   │
│  │  │   │       ┌────────────────────────────────────────────────────┐ │ │ │   │
│  │  │   │       │   MATCH ENCONTRADO                                │ │ │ │   │
│  │  │   │       │   RETORNAR categoría                             │ │ │ │   │
│  │  │   │       └────────────────────────────────────────────────────┘ │ │ │   │
│  │  │   │   FIN SI                                                      │ │ │   │
│  │  │   └─────────────────────────────────────────────────────────────┘ │ │   │
│  │  └───────────────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│           │                                                                     │
│           ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │   NINGÚN MATCH ENCONTRADO                                              │   │
│  │   ┌─────────────────────────────────────────────────────────────────┐   │   │
│  │   │   RETORNAR categoría "Otros" (DEFAULT_CATEGORY)               │   │   │
│  │   └─────────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│           │                                                                     │
│           ▼                                                                     │
│  FIN                                                                          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

### 5.4 StatisticsService (Servicio de Estadísticas)

#### 5.4.1 Responsabilidades

- Calcular métricas agregadas de gastos
- Generar datos para visualización de gráficos
- Proporcionar resúmenes por período y categoría

#### 5.4.2 Interfaz Pública

```python
class StatisticsService:
    """
    Servicio de estadísticas y cálculos agregados de gastos.
    
    Proporciona métricas para el dashboard de visualización,
    incluyendo totales, promedios, y distribuciones por categoría.
    """
    
    def __init__(self, expense_repository: IExpenseRepository):
        """
        Constructor del servicio de estadísticas.
        
        Args:
            expense_repository: Repositorio de gastos para consultas
        """
        self._repository = expense_repository
    
    def get_total_expenses(
        self,
        user_id: str,
        year: int,
        month: int
    ) -> float:
        """
        Calcula el total de gastos para un período específico.
        
        Args:
            user_id: ID del usuario propietario
            year: Año del período
            month: Mes del período
            
        Returns:
            float: Total de gastos del período
        """
        pass
    
    def get_expenses_by_category(
        self,
        user_id: str,
        year: int,
        month: int
    ) -> Dict[str, float]:
        """
        Obtiene la distribución de gastos por categoría.
        
        Args:
            user_id: ID del usuario propietario
            year: Año del período
            month: Mes del período
            
        Returns:
            Dict[str, float]: Diccionario {categoría: total}
        """
        pass
    
    def get_average_expense(
        self,
        user_id: str,
        year: int,
        month: int
    ) -> float:
        """
        Calcula el gasto promedio por transacción.
        
        Args:
            user_id: ID del usuario propietario
            year: Año del período
            month: Mes del período
            
        Returns:
            float: Gasto promedio (0 si no hay gastos)
        """
        pass
    
    def get_expense_count(
        self,
        user_id: str,
        year: int,
        month: int
    ) -> int:
        """
        Cuenta el número de transacciones en un período.
        
        Args:
            user_id: ID del usuario propietario
            year: Año del período
            month: Mes del período
            
        Returns:
            int: Número de transacciones
        """
        pass
    
    def get_top_category(
        self,
        user_id: str,
        year: int,
        month: int
    ) -> Optional[Dict[str, Any]]:
        """
        Identifica la categoría con mayor gasto.
        
        Args:
            user_id: ID del usuario propietario
            year: Año del período
            month: Mes del período
            
        Returns:
            Optional[Dict]: {name, icon, total, percentage} o None si no hay gastos
        """
        pass
    
    def get_daily_average(
        self,
        user_id: str,
        year: int,
        month: int
    ) -> float:
        """
        Calcula el gasto promedio por día en el período.
        
        Args:
            user_id: ID del usuario propietario
            year: Año del período
            month: Mes del período
            
        Returns:
            float: Gasto promedio diario
        """
        pass
    
    def get_statistics_summary(
        self,
        user_id: str,
        year: int,
        month: int
    ) -> Dict[str, Any]:
        """
        Genera un resumen completo de estadísticas.
        
        Args:
            user_id: ID del usuario propietario
            year: Año del período
            month: Mes del período
            
        Returns:
            Dict[str, Any]: Resumen con todas las métricas
        """
        pass
    
    def get_chart_data(
        self,
        user_id: str,
        year: int,
        month: int
    ) -> Dict[str, Any]:
        """
        Genera datos optimizados para渲染 de gráficos.
        
        Args:
            user_id: ID del usuario propietario
            year: Año del período
            month: Mes del período
            
        Returns:
            Dict[str, Any]: Datos formateados para visualización
        """
        pass
```

---

## 6. Patrones de Diseño Implementados

### 6.1 Patrón Repository

#### 6.1.1 Propósito

Abstraer el acceso a los datos, permitiendo cambiar la implementación de persistencia (memoria → base de datos) sin modificar la lógica de negocio.

#### 6.1.2 Diagrama de Clase

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          PATRÓN REPOSITORY                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│    ┌────────────────────────┐                                                   │
│    │   <<interface>>        │                                                   │
│    │   IExpenseRepository   │                                                   │
│    ├────────────────────────┤                                                   │
│    │ + add(expense)         │                                                   │
│    │ + update(expense)      │                                                   │
│    │ + delete(expense_id)   │                                                   │
│    │ + get_by_id(id)        │                                                   │
│    │ + get_by_user(user_id) │                                                   │
│    │ + filter(filters)      │                                                   │
│    └───────────┬────────────┘                                                   │
│                │                                                                │
│                │ implements                                                     │
│                │                                                                │
│    ┌───────────┴────────────┐                                                   │
│    │                        │                                                   │
│    ▼                        ▼                                                   │
│  ┌──────────────────────┐  ┌──────────────────────────────────────────┐        │
│  │  InMemoryExpense      │  │  (Future) DatabaseExpenseRepository      │        │
│  │  Repository           │  │  - SQLite Implementation                 │        │
│  ├──────────────────────┤  ├──────────────────────────────────────────┤        │
│  │  _storage: List[Exp]  │  │  (Future: PostgreSQL, MySQL, etc.)       │        │
│  ├──────────────────────┤  ├──────────────────────────────────────────┤        │
│  │  + add(expense)       │  │  + add(expense)                           │        │
│  │  + update(expense)    │  │  + update(expense)                        │        │
│  │  + delete(expense_id) │  │  + delete(expense_id)                    │        │
│  │  + get_by_id(id)      │  │  + get_by_id(id)                         │        │
│  │  + get_by_user(uid)   │  │  + get_by_user(uid)                      │        │
│  │  + filter(filters)    │  │  + filter(filters)                       │        │
│  └──────────────────────┘  └──────────────────────────────────────────┘        │
│                                                                                 │
│  BENEFICIO: En producción, solo hay que implementar la interfaz                 │
│             y el resto del código funciona sin cambios.                          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### 6.1.3 Interfaz Genérica

```python
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, TypeVar, Generic

T = TypeVar('T')

class IRepository(ABC, Generic[T]):
    """Interfaz base para todos los repositorios."""
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Agrega una nueva entidad al repositorio."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> Optional[T]:
        """Actualiza una entidad existente."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Elimina una entidad por su ID."""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Obtiene una entidad por su ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Obtiene todas las entidades."""
        pass


class IExpenseRepository(IRepository[Expense]):
    """Interfaz específica para repositorio de gastos."""
    
    def get_by_user(self, user_id: str) -> List[Expense]:
        """Obtiene todos los gastos de un usuario."""
        pass
    
    def filter(self, user_id: str, filters: Dict[str, Any]) -> List[Expense]:
        """Filtra gastos por criterios específicos."""
        pass


class IUserRepository(IRepository[User]):
    """Interfaz específica para repositorio de usuarios."""
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Obtiene un usuario por su nombre de usuario."""
        pass
    
    def exists(self, username: str) -> bool:
        """Verifica si existe un usuario con el nombre dado."""
        pass
```

---

### 6.2 Patrón Service Layer

#### 6.2.1 Propósito

Encapsular la lógica de negocio en servicios con operaciones significativas, separándola de la capa de presentación.

#### 6.2.2 Implementación

```python
class BaseService:
    """Clase base para todos los servicios con funcionalidades comunes."""
    
    def __init__(self):
        self._validate_initialization()
    
    def _validate_initialization(self):
        """Valida que el servicio esté correctamente inicializado."""
        pass


class ServiceFactory:
    """Fábrica para crear instancias de servicios con sus dependencias."""
    
    @staticmethod
    def create_services() -> Dict[str, Any]:
        """
        Crea todas las instancias de servicios con sus dependencias inyectadas.
        
        Returns:
            Dict con todas las instancias de servicios
        """
        # Crear repositorios
        user_repository = InMemoryUserRepository()
        expense_repository = InMemoryExpenseRepository()
        category_repository = CategoryRepository()
        
        # Crear servicios con sus dependencias
        categorization_service = CategorizationService(category_repository)
        
        auth_service = AuthService(user_repository)
        
        expense_service = ExpenseService(
            expense_repository=expense_repository,
            categorization_service=categorization_service
        )
        
        statistics_service = StatisticsService(expense_repository)
        
        return {
            'auth': auth_service,
            'expense': expense_service,
            'categorization': categorization_service,
            'statistics': statistics_service
        }
```

---

### 6.3 Patrón Result (Error Handling)

#### 6.3.1 Propósito

Evitar el uso de excepciones para flujo de control normal, utilizando un tipo Result que representa tanto éxito como error.

#### 6.3.2 Implementación

```python
# En utils/result.py

from dataclasses import dataclass
from typing import Any, Optional, TypeVar, Generic

T = TypeVar('T')

@dataclass
class Result(Generic[T]):
    """
    Tipo Result para manejo de errores sin excepciones.
    
    Usage:
        result = service.operation()
        if result.success:
            process(result.data)
        else:
            handle_error(result.error)
    """
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    
    @classmethod
    def ok(cls, data: T = None) -> 'Result[T]':
        """Crea un resultado exitoso."""
        return cls(success=True, data=data)
    
    @classmethod
    def fail(cls, error: str, error_code: str = None) -> 'Result[T]':
        """Crea un resultado de error."""
        return cls(success=False, error=error, error_code=error_code)
    
    @property
    def is_success(self) -> bool:
        """Verifica si el resultado es exitoso."""
        return self.success
    
    @property
    def is_failure(self) -> bool:
        """Verifica si el resultado es un error."""
        return not self.success
```

---

### 6.4 Patrón Dependency Injection

#### 6.4.1 Propósito

Inyectar dependencias en lugar de crearlas internamente, facilitando testing y flexibilidad.

#### 6.4.2 Implementación

```python
class ExpenseService:
    """
    Servicio que recibe sus dependencias vía constructor.
    
    Esto permite:
    1. Testing con mocks/stubs
    2. Cambio de implementación sin modificar el servicio
    3. Ciclo de vida manejado externamente
    """
    
    def __init__(
        self,
        expense_repository: IExpenseRepository,
        categorization_service: CategorizationService,
        validators: Optional[List[Validator]] = None
    ):
        self._repository = expense_repository
        self._categorization = categorization_service
        self._validators = validators or []
    
    def create_expense(self, ...):
        # Usar self._repository y self._categorization
        pass
```

---

## 7. Especificación de la Capa UI (Gradio)

### 7.1 Estructura de Interfaces

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           ESTRUCTURA DE UI (GRADIO)                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  main.py                                                                         │
│  ├── create_app() -> gr.Blocks                                                  │
│  │                                                                               │
│  │   ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │   │                         APP principal                                │   │
│  │   │   (gr.Blocks con autenticación condicional)                        │   │
│  │   ├───────────────────────────────────────────────────────────────────┤   │
│  │   │                                                                   │   │
│  │   │   ESTADO: No autenticado ──────▶ AuthScreen (Login/Register)      │   │
│  │   │                                    │                               │   │
│  │   │                                    │ éxito                        │   │
│  │   │                                    ▼                               │   │
│  │   │   ESTADO: Autenticado ────────▶ MainScreen                        │   │
│  │   │                                    │                               │   │
│  │   │         ┌──────────────────────────┼────────────────────────┐    │   │
│  │   │         │                          │                        │    │   │
│  │   │         ▼                          ▼                        ▼    │   │
│  │   │   ┌──────────────┐          ┌──────────────┐          ┌───────────┐ │   │
│  │   │   │ Registrar    │          │ Ver Gastos   │          │ Estadísticas│ │
│  │   │   │ Gasto        │          │              │          │           │ │   │
│  │   │   ├──────────────┤          ├──────────────┤          ├───────────┤ │   │
│  │   │   │ - Formulario │          │ - Tabla      │          │ - Summary │ │   │
│  │   │   │ - Categoría  │          │ - Filtros    │          │ - Gráfico │ │   │
│  │   │   │   auto       │          │ - Editar     │          │ - Período │ │   │
│  │   │   │ - Botón      │          │ - Eliminar   │          │ - Selector│ │   │
│  │   │   │   guardar   │          │              │          │           │ │   │
│  │   │   └──────────────┘          └──────────────┘          └───────────┘ │   │
│  │   │                                                                   │   │
│  │   └───────────────────────────────────────────────────────────────────┘   │
│  │                                                                               │
│  └─────────────────────────────────────────────────────────────────────────────┘
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Componentes de UI

#### 7.2.1 Pantalla de Autenticación

```python
# ui/auth_ui.py

def create_auth_screen(services: Dict) -> Tuple[gr.Column, Dict]:
    """
    Crea la pantalla de autenticación con login y registro.
    
    Returns:
        Tuple containing the UI component and event handlers
    """
    with gr.Column(visible=True) as auth_screen:
        gr.Markdown("# Gestor de Gastos Personales")
        gr.Markdown("### Inicia sesión o regístrate para continuar")
        
        with gr.Tab("Iniciar Sesión"):
            username_input = gr.Textbox(
                label="Nombre de usuario",
                placeholder="Ingresa tu usuario"
            )
            password_input = gr.Textbox(
                label="Contraseña",
                type="password",
                placeholder="Ingresa tu contraseña"
            )
            login_button = gr.Button("Iniciar Sesión", variant="primary")
            login_output = gr.Textbox(label="Estado", interactive=False)
        
        with gr.Tab("Registrarse"):
            full_name_input = gr.Textbox(
                label="Nombre completo",
                placeholder="Ingresa tu nombre completo"
            )
            new_username_input = gr.Textbox(
                label="Nombre de usuario",
                placeholder="Elige un nombre de usuario"
            )
            new_password_input = gr.Textbox(
                label="Contraseña",
                type="password",
                placeholder="Mínimo 4 caracteres"
            )
            register_button = gr.Button("Crear Cuenta", variant="primary")
            register_output = gr.Textbox(label="Estado", interactive=False)
    
    return auth_screen, {...}  # event handlers
```

#### 7.2.2 Pantalla de Registro de Gastos

```python
# ui/expense_ui.py

def create_expense_form(
    services: Dict,
    state: gr.State
) -> Tuple[gr.Column, Dict]:
    """
    Crea el formulario de registro de gastos.
    """
    with gr.Column(visible=True) as expense_form:
        gr.Markdown("## Registrar Nuevo Gasto")
        
        with gr.Row():
            amount_input = gr.Number(
                label="Monto *",
                placeholder="0.00",
                minimum=0.01,
                precision=2
            )
            date_input = gr.DatePicker(
                label="Fecha *",
                max_date=datetime.now().date()
            )
            category_input = gr.Dropdown(
                label="Categoría (opcional)",
                choices=category_choices,
                value=None
            )
        
        description_input = gr.Textbox(
            label="Descripción",
            placeholder="Ej: Compra en supermercado, Cena de trabajo...",
            max_lines=2
        )
        
        with gr.Row():
            submit_button = gr.Button("Guardar Gasto", variant="primary")
            clear_button = gr.Button("Limpiar", variant="secondary")
        
        result_message = gr.Textbox(
            label="Estado",
            interactive=False,
            visible=False
        )
    
    return expense_form, {...}  # event handlers
```

#### 7.2.3 Dashboard de Estadísticas

```python
# ui/statistics_ui.py

def create_statistics_dashboard(
    services: Dict,
    state: gr.State
) -> Tuple[gr.Column, Dict]:
    """
    Crea el dashboard de estadísticas con gráficos.
    """
    with gr.Column(visible=True) as statistics_dashboard:
        gr.Markdown("## Estadísticas de Gastos")
        
        with gr.Row():
            year_selector = gr.Dropdown(
                label="Año",
                choices=[str(datetime.now().year)],
                value=str(datetime.now().year)
            )
            month_selector = gr.Dropdown(
                label="Mes",
                choices=MONTH_NAMES,
                value=MONTH_NAMES[datetime.now().month - 1]
            )
            refresh_button = gr.Button("Actualizar", variant="primary")
        
        with gr.Row():
            total_card = gr.Number(label="Total de Gastos", interactive=False)
            count_card = gr.Number(label="Transacciones", interactive=False)
            avg_card = gr.Number(label="Promedio por Gasto", interactive=False)
            top_category_card = gr.Textbox(
                label="Categoría Principal",
                interactive=False
            )
        
        gr.Markdown("### Distribución por Categoría")
        pie_chart = gr.Plot()
        
        gr.Markdown("### Gastos por Categoría")
        bar_chart = gr.Plot()
        
        # Mensaje de estado vacío
        empty_message = gr.Markdown(
            "No hay gastos registrados para el período seleccionado.",
            visible=False
        )
    
    return statistics_dashboard, {...}  # event handlers
```

---

## 8. Estrategia de Despliegue

### 8.1 Opciones de Despliegue

#### 8.1.1 Despliegue Local (Desarrollo)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        DESPLIEGUE LOCAL                                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  REQUISITOS:                                                                    │
│  ├── Python 3.9+                                                                │
│  ├── pip (gestor de paquetes)                                                  │
│  └── Git (control de versiones)                                               │
│                                                                                 │
│  PASOS:                                                                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  1. Clonar repositorio                                                  │   │
│  │     $ git clone <repo-url>                                             │   │
│  │     $ cd gastos_personales_prototype                                   │   │
│  │                                                                         │   │
│  │  2. Crear entorno virtual                                               │   │
│  │     $ python -m venv venv                                              │   │
│  │     $ source venv/bin/activate  # Linux/Mac                            │   │
│  │     $ venv\Scripts\activate     # Windows                             │   │
│  │                                                                         │   │
│  │  3. Instalar dependencias                                               │   │
│  │     $ pip install -r requirements.txt                                  │   │
│  │                                                                         │   │
│  │  4. Ejecutar aplicación                                                 │   │
│  │     $ python main.py                                                   │   │
│  │                                                                         │   │
│  │  5. Acceder a la interfaz                                               │   │
│  │     Abrir navegador en: http://localhost:7860                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### 8.1.2 Despliegue en Spaces (Hugging Face) - Recomendado para Prototipo

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        HF SPACES DEPLOYMENT                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  VENTAJAS:                                                                      │
│  ├── Despliegue automático desde GitHub                                        │
│  ├── URL pública gratuita                                                      │
│  ├── No requiere servidor propio                                               │
│  └── Ideal para demos y presentaciones                                        │
│                                                                                 │
│  CONFIGURACIÓN REQUERIDA:                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  requirements.txt                                                       │   │
│  │  ├── gradio>=4.0.0                                                      │   │
│  │  ├── matplotlib>=3.7.0                                                 │   │
│  │  └── (otras dependencias)                                               │   │
│  │                                                                         │   │
│  │  spaces.yaml (metadata)                                                 │   │
│  │  ├── title: "Gestor de Gastos Personales"                              │   │
│  │  ├── emoji: "💰"                                                       │   │
│  │  ├── colorFrom: "green"                                                │   │
│  │  └── colorTo: "blue"                                                   │   │
│  │                                                                         │   │
│  │  README.md (con badge de Spaces)                                        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### 8.1.3 Despliegue en Contenedores (Producción Futura)

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copiar archivos de requisitos primero (para caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Exponer puerto de Gradio
EXPOSE 7860

# Variable de entorno para modo producción
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT="7860"

# Comando de inicio
CMD ["python", "main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  gastos-app:
    build: .
    ports:
      - "7860:7860"
    environment:
      - GRADIO_SERVER_NAME=0.0.0.0
      - GRADIO_SERVER_PORT=7860
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

### 8.2 Configuración de Variables de Entorno

```bash
# .env.example - Variables de entorno para configuración

# =============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# =============================================================================

# Entorno de ejecución (development/staging/production)
APP_ENV=development

# Puerto del servidor
GRADIO_SERVER_PORT=7860

# Host del servidor
GRADIO_SERVER_NAME=0.0.0.0

# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD (para futuras versiones)
# =============================================================================

# Secret key para sesiones (generar con: python -c "import secrets; print(secrets.token_hex(32))")
SECRET_KEY=your-secret-key-here

# =============================================================================
# CONFIGURACIÓN DE BASE DE DATOS (para versión futura)
# =============================================================================

# Tipo de base de datos (sqlite/postgresql/mysql)
DB_TYPE=sqlite

# Connection string
DB_CONNECTION=sqlite:///gastos.db
```

---

### 8.3 Pipeline CI/CD

```yaml
# .github/workflows/ci.yml

name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Spaces
      run: |
        # Script de despliegue a HuggingFace Spaces
        echo "Desplegando a HuggingFace Spaces..."
```

---

## 9. Justificación de Decisiones Técnicas

### 9.1 Selección de Tecnología

#### 9.1.1 Python como Lenguaje Backend

| Criterio | Evaluación | Justificación |
|----------|------------|---------------|
| **Requisito del cliente** | ✅ Cumplido | Python es tecnología solicitada explícitamente |
| **Curva de aprendizaje** | ✅ Baja | Sintaxis simple, legible, fácil de mantener |
| **Ecosistema** | ✅ Excelente | Gran cantidad de librerías para data/ML |
| **Comunidad** | ✅ Activa | Amplia comunidad, documentación extensiva |
| **Rendimiento** | ⚠️ Aceptable | Suficiente para prototipo y volúmenes pequeños-medios |

**Decisión**: Se selecciona Python 3.9+ por ser el lenguaje requerido y por su idoneidad para el prototipado rápido.

#### 9.1.2 Gradio como Framework Frontend

| Criterio | Evaluación | Justificación |
|----------|------------|---------------|
| **Requisito del cliente** | ✅ Cumplido | Gradio es tecnología solicitada |
| **Velocidad de desarrollo** | ✅ Excelente | Permite crear UI funcionales en minutos |
| **Visualizaciones** | ✅ Soportado | Integración nativa con matplotlib |
| **Personalización** | ⚠️ Limitada | Menos flexible que frameworks web tradicionales |
| **Producción lista** | ✅ Disponible | HuggingFace Spaces ofrece hosting gratuito |

**Decisión**: Se selecciona Gradio por su integración con Python, velocidad de prototipado, y capacidades de visualización integradas.

#### 9.1.3 Almacenamiento en Memoria

| Criterio | Evaluación | Justificación |
|----------|------------|---------------|
| **Simplicidad** | ✅ Excelente | Sin configuración de base de datos |
| **Prototipo** | ✅ Ideal | Perfecto para demos rápidas |
| **Escalabilidad** | ⚠️ Limitada | No adecuado para producción con muchos datos |
| **Persistencia** | ❌ Nula | Los datos se pierden al cerrar |

**Decisión**: Se utiliza almacenamiento en memoria para el prototipo, con la arquitectura preparada (patrón Repository) para migración futura a base de datos.

---

### 9.2 Patrones de Diseño

#### 9.2.1 Layered Architecture

```
JUSTIFICACIÓN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. SEPARACIÓN DE CONCERNS
   ├── UI: Concentra en presentación e interacción de usuario
   ├── Services: Lógica de negocio y reglas de aplicación
   └── Data: Acceso y persistencia de datos

2. MANTENIBILIDAD
   └── Cambios en una capa no afectan las demás
   
3. TESTABILIDAD
   └── Cada capa puede probarse independientemente con mocks

4. ESCALABILIDAD
   └── Preparado para crecimiento: agregar cache, workers, etc.
```

#### 9.2.2 Repository Pattern

```
JUSTIFICACIÓN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ABSTRACCIÓN DE PERSISTENCIA
   El código de negocio no conoce cómo se almacenan los datos.
   
2. MIGRACIÓN FUTURA
   Para pasar de memoria a SQL o NoSQL, solo se implementa
   una nueva clase que implemente la interfaz.
   
3. TESTING
   Los tests pueden usar repositorios en memoria (mock)
   sin necesidad de una base de datos real.
   
4. CONTRATO CLARO
   La interfaz define exactamente qué operaciones están disponibles.
```

#### 9.2.3 Dependency Injection

```
JUSTIFICACIÓN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. FLEXIBILIDAD
   Las dependencias pueden cambiarse sin modificar las clases que las usan.

2. TESTING
   Se pueden inyectar mocks/stubs para probar en aislamiento.

3. SINGLE RESPONSIBILITY
   Las clases no crean sus dependencias, solo las usan.

4. DECOUPLED DESIGN
   Los componentes están débilmente acoplados entre sí.
```

---

### 9.3 Decisiones de Seguridad

#### 9.3.1 Para el Prototipo

| Aspecto | Implementación | Razón |
|---------|----------------|-------|
| Contraseñas | Texto plano (en memoria) | Prototipo sin exposición real |
| Sesiones | State de Gradio | Suficiente para demo |
| Validación | Servidor y cliente | UX responsiva |

#### 9.3.2 Recomendaciones para Producción

| Aspecto | Recomendación | Prioridad |
|---------|---------------|----------|
| Contraseñas | Hashing con bcrypt/argon2 | Alta |
| Autenticación | JWT tokens | Alta |
| HTTPS | Obligatorio | Alta |
| Rate Limiting | Implementar | Media |
| SQL Injection | Usar ORM | Alta |
| XSS | Sanitización | Media |

---

### 9.4 Decisiones de Rendimiento

| Operación | Estimación | Justificación |
|-----------|------------|---------------|
| Inicio de app | < 3 segundos | Carga de módulos y Gradio |
| Login/Logout | < 100ms | Operaciones en memoria |
| CRUD Gastos | < 50ms | Operaciones en listas |
| Estadísticas | < 500ms | Cálculos en memoria |
| Gráficos | < 1 segundo | Renderizado matplotlib |

**Optimizaciones implementadas**:
- Lazy loading de módulos no esenciales
- Cálculo de estadísticas en demanda (no pre-computadas)
- Renderizado de gráficos con caching de matplotlib

---

## 10. Diagrama de Componentes del Sistema

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      DIAGRAMA DE COMPONENTES                                    │
│                      (Component Diagram - C4 Level 2)                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                         USUARIO                                          │   │
│  │                    (Actor Externo)                                      │   │
│  │                                                                          │   │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │   │
│  │   │  Login  │  │Registrar│  │  Ver    │  │  Editar │  │  Ver    │      │   │
│  │   │  Gastos │  │ Gasto   │  │ Gastos  │  │ Gasto   │  │ Stats   │      │   │
│  │   └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘      │   │
│  └────────┼────────────┼────────────┼────────────┼────────────┼───────────┘   │
│           │            │            │            │            │               │
│           ▼            ▼            ▼            ▼            ▼               │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    SISTEMA: GESTOR DE GASTOS                            │   │
│  │                                                                          │   │
│  │   ┌─────────────────────────────────────────────────────────────────┐    │   │
│  │   │                    CAPA DE PRESENTACIÓN                        │    │   │
│  │   │  ┌───────────────┐  ┌───────────────┐  ┌───────────────────┐  │    │   │
│  │   │  │  AuthUI       │  │  ExpenseUI   │  │  StatisticsUI     │  │    │   │
│  │   │  │  Component    │  │  Component   │  │  Component       │  │    │   │
│  │   │  └───────┬───────┘  └───────┬───────┘  └────────┬────────┘  │    │   │
│  │   │          │                  │                   │           │    │   │
│  │   └──────────┼──────────────────┼───────────────────┼──────────┘    │   │
│  │              │                  │                   │                 │   │
│  │              ▼                  ▼                   ▼                 │   │
│  │   ┌─────────────────────────────────────────────────────────────────┐    │   │
│  │   │                    CAPA DE SERVICIOS                          │    │   │
│  │   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────┐ │    │   │
│  │   │  │ AuthService │  │ExpenseServ. │  │CategoryServ │  │Stats │ │    │   │
│  │   │  │             │  │             │  │             │  │Serv. │ │    │   │
│  │   │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──┬───┘ │    │   │
│  │   │         │                │                │            │     │    │   │
│  │   └─────────┼────────────────┼────────────────┼────────────┼─────┘    │   │
│  │             │                │                │            │          │   │
│  │             ▼                ▼                ▼            │          │   │
│  │   ┌───────────────────────────────────────────────────────────────┐    │   │
│  │   │                    CAPA DE DATOS                              │    │   │
│  │   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐│    │   │
│  │   │  │    User     │  │   Expense   │  │      Category          ││    │   │
│  │   │  │  Repository │  │  Repository │  │     Repository        ││    │   │
│  │   │  └──────┬──────┘  └──────┬──────┘  └─────────────────────────┘│    │   │
│  │   │         │                │                                   │    │   │
│  │   └─────────┼────────────────┼───────────────────────────────────┘    │   │
│  │             │                │                                      │   │
│  │             ▼                ▼                                      │   │
│  │   ┌───────────────────────────────────────────────────────────────┐    │   │
│  │   │               INFRAESTRUCTURA DE DATOS                       │    │   │
│  │   │                                                               │    │   │
│  │   │    ┌─────────────────┐      ┌─────────────────┐              │    │   │
│  │   │    │   users_db     │      │   expenses_db   │              │    │   │
│  │   │    │   (Dict)       │      │   (List)        │              │    │   │
│  │   │    └─────────────────┘      └─────────────────┘              │    │   │
│  │   │                                                               │    │   │
│  │   └───────────────────────────────────────────────────────────────┘    │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Lista de Dependencias del Proyecto

### 11.1 requirements.txt

```
# =============================================================================
# DEPENDENCIAS PRINCIPALES
# =============================================================================

# Framework web para prototipado de interfaces
gradio>=4.0.0

# Librería para visualizaciones y gráficos
matplotlib>=3.7.0

# Utilidades para manejo de fechas
python-dateutil>=2.8.0

# =============================================================================
# DEPENDENCIAS DE DESARROLLO (opcional)
# =============================================================================

# Framework de testing
pytest>=7.0.0

# Plugin de cobertura para pytest
pytest-cov>=4.0.0

# Type checking
mypy>=1.0.0

# Linting
flake8>=6.0.0
```

### 11.2 Estructura de Archivos del Proyecto

```
gastos_personales_prototype/
│
├── main.py                         # Punto de entrada de la aplicación
│
├── requirements.txt                # Dependencias de Python
│
├── .env.example                    # Variables de entorno de ejemplo
│
├── README.md                       # Documentación del proyecto
│
├── config/                         # Configuración del sistema
│   ├── __init__.py
│   └── categories.py              # Configuración de categorías
│
├── models/                         # Modelos de dominio
│   ├── __init__.py
│   ├── base.py                    # Clases base (Result, etc.)
│   ├── user.py                    # Modelo de Usuario
│   ├── expense.py                 # Modelo de Gasto
│   └── category.py                # Modelo de Categoría
│
├── services/                       # Lógica de negocio
│   ├── __init__.py
│   ├── auth_service.py            # Servicio de autenticación
│   ├── expense_service.py         # Servicio de gestión de gastos
│   ├── categorization_service.py  # Servicio de categorización
│   └── statistics_service.py      # Servicio de estadísticas
│
├── repositories/                   # Capa de acceso a datos
│   ├── __init__.py
│   ├── base.py                    # Interfaces de repositorio
│   ├── user_repository.py         # Repositorio de usuarios
│   ├── expense_repository.py      # Repositorio de gastos
│   └── category_repository.py     # Repositorio de categorías
│
├── ui/                             # Componentes de interfaz
│   ├── __init__.py
│   ├── app.py                     # Aplicación principal de Gradio
│   ├── auth_ui.py                # Interfaz de autenticación
│   ├── expense_ui.py             # Interfaz de gestión de gastos
│   ├── statistics_ui.py         # Interfaz de estadísticas
│   └── components.py            # Componentes reutilizables
│
├── utils/                          # Utilidades
│   ├── __init__.py
│   ├── validators.py             # Funciones de validación
│   ├── helpers.py               # Funciones auxiliares
│   └── constants.py             # Constantes del sistema
│
├── tests/                          # Suite de pruebas
│   ├── __init__.py
│   ├── conftest.py              # Configuración de pytest
│   ├── test_auth_service.py
│   ├── test_expense_service.py
│   ├── test_categorization.py
│   ├── test_statistics_service.py
│   └── test_validators.py
│
└── docs/                           # Documentación adicional
    ├── architecture.md
    ├── api_reference.md
    └── deployment.md
```

---

## 12. Consideraciones de Mantenibilidad

### 12.1 Convenciones de Código

```python
# =============================================================================
# CONVENCIONES DE CÓDIGO - PEP 8 + TYPE HINTS
# =============================================================================

# Nomenclatura
# -----------
# Clases: PascalCase (User, ExpenseService)
# Funciones/métodos: snake_case (get_user_by_id)
# Constantes: UPPER_SNAKE_CASE (MAX_DESCRIPTION_LENGTH)
# Variables: snake_case (current_user)
# Módulos: snake_case (auth_service.py)

# Type Hints
# ----------
def create_expense(
    self,
    user_id: str,
    amount: float,
    description: Optional[str] = None
) -> Result[Expense]:
    """Crea un nuevo gasto para el usuario."""
    pass

# Docstrings - Google Style
# ------------------------
def calculate_total(self, user_id: str, period: Period) -> float:
    """
    Calcula el total de gastos para un período específico.
    
    Args:
        user_id: Identificador único del usuario.
        period: Período de tiempo a consultar.
        
    Returns:
        float: Total de gastos sumados.
        
    Raises:
        ValueError: Si el período es inválido.
    """
    pass
```

### 12.2 Documentación Requerida

| Componente | Docstrings | Type Hints | Tests |
|------------|------------|------------|-------|
| Clases modelo | ✅ Requerido | ✅ Requerido | ✅ Mínimo 80% cobertura |
| Servicios | ✅ Requerido | ✅ Requerido | ✅ Unit tests |
| Repositorios | ✅ Requerido | ✅ Requerido | ✅ Integración |
| UI Components | ✅ Básico | ⚠️ Opcional | ⚠️ Manual |
| Utils | ✅ Requerido | ✅ Requerido | ✅ Unit tests |

---

## 13. Glosario Técnico

| Término | Definición |
|---------|------------|
| **Layered Architecture** | Patrón arquitectónico que separa el código en capas (UI, Business, Data) |
| **Repository Pattern** | Patrón que abstrae el acceso a datos, ocultando la implementación de persistencia |
| **Dependency Injection** | Técnica donde las dependencias se pasan al constructor en lugar de crearse internamente |
| **Result Type** | Tipo que representa el resultado de una operación, conteniendo éxito o error |
| **State Management** | Gestión del estado de la aplicación, especialmente en frameworks UI |
| **C4 Model** | Metodología de documentación de arquitectura de software en 4 niveles |
| **PEP 8** | Guía de estilo para código Python |
| **Type Hints** | Anotaciones de tipo estático en Python 3.5+ |
| **Dataclass** | Decorador en Python que genera automáticamente __init__, __repr__, etc. |

---

## 14. Referencias y Estándares

| Estándar | Descripción |
|----------|-------------|
| **PEP 8** | Style Guide for Python Code |
| **PEP 257** | Docstring Conventions |
| **PEP 484** | Type Hints |
| **PEP 526** | Syntax for Variable Annotations |
| **gRPC Design** | API Design Patterns |
| **C4 Model** | Software Architecture Documentation (Simon Brown) |

---

## 15. Aprobaciones

| Rol | Nombre | Fecha | Firma |
|-----|--------|-------|-------|
| Tech Lead | [TBD] | [Fecha] | ____________ |
| Scrum Master | [TBD] | [Fecha] | ____________ |
| Equipo de Desarrollo | [TBD] | [Fecha] | ____________ |

---

## 16. Historial de Versiones

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | Enero 2025 | Tech Lead | Versión inicial del documento |

---

*Este documento complementa el PRD y sirve como guía técnica para la implementación del prototipo.*