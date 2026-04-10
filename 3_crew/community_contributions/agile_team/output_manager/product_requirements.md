# Producto Requirements Document (PRD)
## Prototipo de Aplicación de Gastos Personales

---

## 1. Información General del Documento

| Campo | Detalle |
|-------|---------|
| **Versión del Documento** | 1.0 |
| **Fecha de Creación** | Enero 2025 |
| **Autor** | Scrum Master / Product Owner |
| **Estado** | Aprobado para Desarrollo |
| **Última Actualización** | Enero 2025 |

---

## 2. Resumen Ejecutivo

### 2.1 Descripción del Producto

Este documento establece los requerimientos completos para el desarrollo de un **prototipo funcional** de una aplicación de gestión de gastos personales. El objetivo principal es demostrar la viabilidad de la idea a la dirección ejecutiva mediante una aplicación operativa que muestre las funcionalidades core: registro de gastos, categorización automática y visualización de estadísticas.

### 2.2 Justificación del Prototipo

Dado que el cliente solicita únicamente un prototipo para presentación ejecutiva, este documento se enfoca en:

- Demostrar el concepto de manera tangible y operativa
- Validar la experiencia de usuario intended
- Mostrar el flujo completo de uso de la aplicación
- Proporcionar una base sólida para futuras implementaciones con persistencia de datos
- Minimizar el tiempo de desarrollo mientras se maximiza el valor demonstrable

### 2.3 Alcance del Prototipo vs. Versión de Producción

| Aspecto | Prototipo | Producción Futura |
|---------|-----------|-------------------|
| Almacenamiento de datos | En memoria (sesión) | Base de datos relacional/NoSQL |
| Autenticación | Simplificada (simulada) | Autenticación real con hashing |
| Persistencia | No persistente | Datos guardados permanentemente |
| Usuarios | Un solo usuario simulado | Multi-usuario |
| Escalabilidad | Limitada | Alta escalabilidad |

---

## 3. Objetivos del Producto

### 3.1 Objetivos Principales

1. **Facilitar el registro de gastos** de manera rápida e intuitiva
2. **Categorizar automáticamente** los gastos según palabras clave y patrones predefinidos
3. **Visualizar estadísticas** de gastos de forma clara y comprensible
4. **Demostrar escalabilidad** en la arquitectura del backend para futuras expansiones
5. **Proporcionar una interfaz de usuario** moderna, responsiva y fácil de usar

### 3.2 Objetivos Secundarios

- Reducir el tiempo que los usuarios destinan al registro manual de gastos
- Educar a los usuarios sobre sus hábitos de consumo mediante visualizaciones
- Identificar patrones de gasto innecesarios o excesivos
- Establecer una base técnica sólida para implementaciones futuras

---

## 4. Definición del Producto

### 4.1 Propuesta de Valor

> "Gestiona tus finanzas personales de manera inteligente: registra tus gastos en segundos, deja que la categorización automática los organice, y descubre insights valiosos sobre tus hábitos de consumo a través de visualizaciones claras e intuitivas."

### 4.2 Descripción de la Solución

La aplicación consiste en un sistema de gestión de gastos personales basado en Python y Gradio que permite:

- **Autenticación simplificada**: Sistema de login/registro básico que simula la experiencia de usuario
- **Registro de gastos**: Formulario intuitivo para capturar gastos con descripción, monto y fecha
- **Categorización automática**: Algoritmo inteligente que clasifica los gastos en categorías predefinidas
- **Dashboard de estadísticas**: Visualizaciones gráficas del comportamiento de gastos mensuales

### 4.3 Tecnología Seleccionada

| Componente | Tecnología | Justificación |
|------------|------------|---------------|
| **Backend** | Python 3.9+ | Lenguaje requerido por el cliente, versátil y con amplio soporte |
| **Frontend** | Gradio | Framework requerido por el cliente, permite prototipado rápido de interfaces |
| **Almacenamiento** | Estructuras en memoria (Python) | Para el prototipo, sin persistencia de datos |
| **Visualización** | Matplotlib/Gradio Charts | Integración nativa con Gradio |
| **Estructura del proyecto** | POO con clases bien definidas | Escalabilidad futura del código |

---

## 5. Alcance del Proyecto

### 5.1 Funcionalidades Incluidas (IN SCOPE)

#### 5.1.1 Sistema de Autenticación
- Pantalla de login con validación de credenciales simuladas
- Pantalla de registro de nuevos usuarios (simulado)
- Gestión de sesión de usuario
- Opción de logout

#### 5.1.2 Gestión de Gastos
- Formulario de registro de nuevo gasto
- Campos obligatorios: descripción, monto, fecha, categoría (opcional manual)
- Categorización automática basada en palabras clave
- Lista de gastos registrados en la sesión actual
- Opción de eliminar gastos individuales
- Edición de gastos existentes

#### 5.1.3 Categorización Automática
- Categorías predefinidas del sistema:
  - 🏠 **Vivienda**: Alquiler, hipoteca, servicios públicos, mantenimiento
  - 🍔 **Alimentación**: Comidas, supermercado, restaurantes,外卖
  - 🚗 **Transporte**: Gasolina, transporte público, mantenimiento vehicular, estacionamiento
  - 🎮 **Entretenimiento**: Cine, streaming, videojuegos, actividades recreativas
  - 🛒 **Compras**: Ropa,electronics, artículos del hogar, compras varias
  - 💊 **Salud**: Medicamentos, consultas médicas, seguro de salud,健身房
  - 📚 **Educación**: Cursos, libros, suscripciones, formación
  - 💰 **Otros**: Gastos no categorizados automáticamente

#### 5.1.4 Visualización de Estadísticas
- Resumen mensual de gastos totales
- Gráfico de categorías (pastel o barras)
- Comparativa de gastos por período
- Tendencia de gastos semanal/quinzenal

### 5.2 Funcionalidades Excluidas (OUT OF SCOPE)

| Funcionalidad Excluida | Razón |
|------------------------|-------|
| Base de datos real | Prototipo sin persistencia |
| Exportación de datos (PDF/Excel) | Puede implementarse en versión completa |
| Notificaciones/reminders | No requerido para el prototipo |
| Presupuestos y límites | Puede añadirse en fase posterior |
| Integración con bancos/API financieras | Fase de producción futura |
| Multi-moneda | Una sola moneda para el prototipo |
| Categorías personalizadas por usuario | Implementación futura |
| Gráficos avanzados/análisis predictivo | Fase de producción |
| Aplicación móvil nativa | Versión web como prueba de concepto |
| Autenticación de dos factores | Simplificación para prototipo |
| Recuperación de contraseña | Simulación básica de auth |
| Roles y permisos múltiples | Un solo usuario simulado |

---

## 6. Requerimientos Funcionales

### 6.1 RF-01: Sistema de Autenticación

**Descripción**: El sistema debe proporcionar un mecanismo de login y registro básico que simule la experiencia de autenticación real.

**Detalle de Requerimientos**:

| ID | Requerimiento | Prioridad | Tipo |
|----|---------------|----------|------|
| RF-01.01 | El sistema mostrará una pantalla inicial con opciones de Login y Registro | Alta | Core |
| RF-01.02 | El formulario de login requerirá: nombre de usuario y contraseña | Alta | Core |
| RF-01.03 | El formulario de registro requerirá: nombre completo, nombre de usuario, contraseña | Alta | Core |
| RF-01.04 | Las contraseñas deberán tener un mínimo de 4 caracteres | Media | Validación |
| RF-01.05 | El sistema mostrará mensajes de error apropiados para credenciales inválidas | Alta | UX |
| RF-01.06 | Tras login exitoso, el sistema mostrará la interfaz principal de gestión de gastos | Alta | Core |
| RF-01.07 | El sistema permitirá cerrar sesión y volver a la pantalla de login | Alta | Core |

**Comportamiento Esperado**:
- El usuario puede crear una cuenta con datos válidos
- El usuario puede iniciar sesión con credenciales registradas
- El sistema mantiene la sesión activa mientras el usuario interactúa
- El logout limpia el estado de la sesión

---

### 6.2 RF-02: Registro de Gastos

**Descripción**: El usuario debe poder registrar nuevos gastos de manera rápida y sencilla.

**Detalle de Requerimientos**:

| ID | Requerimiento | Prioridad | Tipo |
|----|---------------|----------|------|
| RF-02.01 | El formulario de registro aceptará: descripción del gasto, monto, fecha | Alta | Core |
| RF-02.02 | El campo de descripción será de texto libre con máximo 200 caracteres | Media | Validación |
| RF-02.03 | El campo de monto aceptará solo valores numéricos positivos con 2 decimales | Alta | Validación |
| RF-02.04 | El campo de fecha permitirá seleccionar fechas no futuras al día actual | Media | Validación |
| RF-02.05 | El usuario podrá especificar manualmente una categoría (opcional) | Media | Feature |
| RF-02.06 | Si no se especifica categoría, el sistema aplicará categorización automática | Alta | Core |
| RF-02.07 | Tras registrar un gasto, el formulario se limpiará y mostrará confirmación | Alta | UX |
| RF-02.08 | El gasto registrado aparecerá inmediatamente en la lista de gastos | Alta | Core |

**Comportamiento Esperado**:
- El usuario llena el formulario con los datos del gasto
- El sistema valida los datos ingresados
- El sistema aplica categorización automática si no se especifica categoría
- El gasto se añade a la lista en memoria
- Se muestra feedback visual de éxito

---

### 6.3 RF-03: Categorización Automática de Gastos

**Descripción**: El sistema debe analizar automáticamente la descripción del gasto y asignarlo a una categoría predefinida.

**Detalle de Requerimientos**:

| ID | Requerimiento | Prioridad | Tipo |
|----|---------------|----------|------|
| RF-03.01 | El sistema utilizará palabras clave para clasificar gastos automáticamente | Alta | Core |
| RF-03.02 | El sistema tendrá una base de datos de palabras clave por categoría | Alta | Core |
| RF-03.03 | Si no hay coincidencia de palabras clave, el gasto se categorizará como "Otros" | Media | Lógica |
| RF-03.04 | El usuario podrá visualizar y modificar la categoría asignada | Alta | Feature |
| RF-03.05 | El sistema considerará tanto mayúsculas como minúsculas indistintamente | Media | Técnica |
| RF-03.06 | Palabras clave parciales (contains) serán consideradas para la match | Media | Técnica |

**Base de Palabras Clave por Categoría**:

```
Vivienda: ["alquiler", "hipoteca", "luz", "agua", "gas", "internet", "teléfono", "mantenimiento", "reforma", "muebles"]
Alimentación: ["comida", "supermercado", "restaurante", "cena", "almuerzo", "desayuno", "fruta", "verdura", "carne", "pescado", "pan", "leche", "cafe", "外卖", "delivery"]
Transporte: ["gasolina", "diesel", "taxi", "uber", "bus", "metro", "tren", "estacionamiento", "peaje", "mantenimiento coche", "neumáticos", "seguro coche"]
Entretenimiento: ["cine", "netflix", "spotify", "amazon prime", "videojuego", "juego", "concierto", "teatro", "museo", "excursión", "viaje", "vacaciones"]
Compras: ["ropa", "zapatos", "electrónica", "teléfono", "computadora", "tablet", "hogar", "decoración", "regalo", "amazon", "tienda"]
Salud: ["médico", "farmacia", "medicina", "doctor", "dentista", "psicólogo", "gimnasio", "fitness", "yoga", "deporte", "seguro médico"]
Educación: ["curso", "universidad", "libro", "escuela", "formación", "certificación", "suscripción", "revista", "periodico", "audiolibro"]
```

---

### 6.4 RF-04: Visualización de Estadísticas

**Descripción**: El sistema debe proporcionar visualizaciones claras y comprensibles de los gastos registrados.

**Detalle de Requerimientos**:

| ID | Requerimiento | Prioridad | Tipo |
|----|---------------|----------|------|
| RF-04.01 | El dashboard mostrará el total de gastos del mes actual | Alta | Core |
| RF-04.02 | Se mostrará un gráfico de pastel con distribución por categorías | Alta | Core |
| RF-04.03 | Se mostrará un gráfico de barras con gastos por categoría | Media | Feature |
| RF-04.04 | El usuario podrá seleccionar el mes/año a visualizar | Media | Feature |
| RF-04.05 | Se mostrará el gasto promedio por día del período seleccionado | Media | Feature |
| RF-04.06 | Se mostrará la categoría con mayor gasto destacada | Media | Insight |
| RF-04.07 | Los datos se actualizarán en tiempo real tras añadir/modificar/eliminar gastos | Alta | UX |

**Métricas a Mostrar**:
- Total de gastos del período
- Número de transacciones registradas
- Promedio de gasto por transacción
- Gasto máximo y mínimo
- Comparativa con período anterior (si hay datos)
- Top 3 categorías con mayor gasto

---

### 6.5 RF-05: Gestión de Gastos Registrados

**Descripción**: El usuario debe poder visualizar, editar y eliminar los gastos registrados.

**Detalle de Requerimientos**:

| ID | Requerimiento | Prioridad | Tipo |
|----|---------------|----------|------|
| RF-05.01 | Se mostrará una tabla/lista con todos los gastos registrados | Alta | Core |
| RF-05.02 | Cada gasto mostrará: fecha, descripción, categoría, monto | Alta | Core |
| RF-05.03 | El usuario podrá editar cualquier campo de un gasto existente | Alta | Feature |
| RF-05.04 | El usuario podrá eliminar un gasto con confirmación | Alta | Feature |
| RF-05.05 | La lista permitirá filtrar por categoría | Media | Feature |
| RF-05.06 | La lista permitirá filtrar por rango de fechas | Media | Feature |
| RF-05.07 | Los cambios se reflejarán inmediatamente en las estadísticas | Alta | UX |

---

## 7. Requerimientos No Funcionales

### 7.1 RNF-01: Usabilidad

| ID | Requerimiento | Criterio de Aceptación |
|----|---------------|------------------------|
| RNF-01.01 | La interfaz debe ser intuitiva y auto-explicativa | Un usuario nuevo debe poder usar la app sin ayuda en menos de 2 minutos |
| RNF-01.02 | El diseño será limpio y profesional | Navegación clara entre secciones |
| RNF-01.03 | Los mensajes de error serán claros y útiles | El usuario sabrá exactamente qué corregir |
| RNF-01.04 | El tiempo de respuesta será instantáneo | Operaciones completas en menos de 1 segundo |

### 7.2 RNF-02: Rendimiento

| ID | Requerimiento | Criterio de Aceptación |
|----|---------------|------------------------|
| RNF-02.01 | La aplicación cargará rápidamente | Tiempo de inicio < 5 segundos |
| RNF-02.02 | Las operaciones de CRUD serán inmediatas | Sin delay perceptible por el usuario |
| RNF-02.03 | Los gráficos se generarán sin delays | Renderizado < 2 segundos |

### 7.3 RNF-03: Arquitectura y Escalabilidad

| ID | Requerimiento | Criterio de Aceptación |
|----|---------------|------------------------|
| RNF-03.01 | El código seguirá principios de POO | Clases bien definidas con responsabilidades únicas |
| RNF-03.02 | La estructura del proyecto será modular | Fácil identificación de componentes |
| RNF-03.03 | El código será documentado | Docstrings en todas las clases y métodos públicos |
| RNF-03.04 | El sistema permitirá añadir nuevas categorías fácilmente | Sin修改 al código core, solo configuración |
| RNF-03.05 | La arquitectura soportará migración a base de datos | Interfaces abstrayendo el acceso a datos |

### 7.4 RNF-04: Mantenibilidad

| ID | Requerimiento | Criterio de Aceptación |
|----|---------------|------------------------|
| RNF-04.01 | El código seguirá PEP 8 | Estilo consistente en todo el proyecto |
| RNF-04.02 | Se utilizarán type hints donde sea posible | Mejor legibilidad y detección de errores |
| RNF-04.03 | Las funciones/métodos serán pequeños y enfocados | Máximo 50 líneas por función (ideal) |

### 7.5 RNF-05: Compatibilidad

| ID | Requerimiento | Criterio de Aceptación |
|----|---------------|------------------------|
| RNF-05.01 | La aplicación funcionará en navegadores modernos | Chrome, Firefox, Safari, Edge |
| RNF-05.02 | Compatible con Python 3.9+ | Sin features de versiones superiores requeridas |

---

## 8. Historias de Usuario

### 8.1 Épica 1: Autenticación de Usuario

---

#### HU-01: Iniciar Sesión en la Aplicación

**Como** usuario registrado,  
**Quiero** poder iniciar sesión con mi nombre de usuario y contraseña,  
**Para** acceder a mi información de gastos de forma segura.

**Criterios de Aceptación**:

```
DADO que soy un usuario registrado en el sistema
Y he proporcionado un nombre de usuario válido
Y he proporcionado una contraseña correcta
CUANDO hago clic en el botón "Iniciar Sesión"
ENTONCES seré redirigido a la interfaz principal de gestión de gastos
Y veré un mensaje de bienvenida personalizado
```

```
DADO que soy un usuario registrado en el sistema
Y he proporcionado credenciales incorrectas
CUANDO hago clic en el botón "Iniciar Sesión"
ENTONCES veré un mensaje de error indicando "Credenciales inválidas"
Y permaneceré en la pantalla de login
```

** Definition of Done**:
- [ ] Pantalla de login visible y funcional
- [ ] Validación de credenciales implemented
- [ ] Mensajes de error apropiados mostrados
- [ ] Redirección exitosa tras login válido
- [ ] Tests unitarios pasando

---

#### HU-02: Registrar una Nueva Cuenta

**Como** nuevo usuario,  
**Quiero** poder crear una cuenta en la aplicación,  
**Para** comenzar a registrar y gestionar mis gastos personales.

**Criterios de Aceptación**:

```
DADO que soy un nuevo usuario
Y proporciono un nombre completo válido (mínimo 3 caracteres)
Y proporciono un nombre de usuario único (mínimo 4 caracteres)
Y proporciono una contraseña válida (mínimo 4 caracteres)
CUANDO hago clic en el botón "Registrarse"
ENTONCES se creará mi cuenta exitosamente
Y seré redirigido automáticamente a la pantalla de login
Y veré un mensaje de confirmación
```

```
DADO que soy un nuevo usuario
Y intento registrarme con un nombre de usuario ya existente
CUANDO hago clic en el botón "Registrarse"
ENTONCES veré un mensaje de error indicando "El usuario ya existe"
Y permaneceré en la pantalla de registro
```

** Definition of Done**:
- [ ] Formulario de registro con validación
- [ ] Creación de usuario en memoria funcional
- [ ] Verificación de usuario único
- [ ] Feedback visual de éxito/error
- [ ] Tests unitarios pasando

---

#### HU-03: Cerrar Sesión

**Como** usuario logueado,  
**Quiero** poder cerrar sesión,  
**Para** asegurar mi información cuando termine de usar la aplicación.

**Criterios de Aceptación**:

```
DADO que estoy logueado en la aplicación
Y accedo a la opción de "Cerrar Sesión"
CUANDO hago clic en el botón "Cerrar Sesión"
ENTONCES mi sesión será finalizada
Y seré redirigido a la pantalla de login
Y mis datos de gastos de esta sesión seguirán disponibles hasta reiniciar la app
```

** Definition of Done**:
- [ ] Botón de logout visible y accesible
- [ ] Sesión limpiada correctamente
- [ ] Redirección a login funcional
- [ ] Tests unitarios pasando

---

### 8.2 Épica 2: Gestión de Gastos

---

#### HU-04: Registrar un Nuevo Gasto

**Como** usuario,  
**Quiero** poder registrar un nuevo gasto con descripción y monto,  
**Para** mantener un registro detallado de mis gastos.

**Criterios de Aceptación**:

```
DADO que estoy logueado en la aplicación
Y accedo a la sección "Registrar Gasto"
Y proporciono una descripción del gasto (ej: "Compra en supermercado")
Y proporciono un monto válido (ej: 45.99)
Y selecciono la fecha del gasto
CUANDO hago clic en el botón "Guardar Gasto"
ENTONCES el gasto será registrado exitosamente
Y aparecerá en la lista de gastos
Y las estadísticas se actualizarán automáticamente
Y veré un mensaje de confirmación
```

```
DADO que estoy logueado en la aplicación
Y accedo a la sección "Registrar Gasto"
Y NO proporciono el campo de monto
CUANDO intento guardar el gasto
ENTONCES veré un mensaje de error indicando que el monto es requerido
Y el gasto no será guardado
```

** Definition of Done**:
- [ ] Formulario de registro de gastos funcional
- [ ] Validación de campos obligatorios
- [ ] Gasto añadido a la lista en memoria
- [ ] Estadísticas actualizadas en tiempo real
- [ ] Mensaje de confirmación mostrado
- [ ] Tests unitarios pasando

---

#### HU-05: Categorización Automática de Gastos

**Como** usuario,  
**Quiero** que el sistema categorice automáticamente mis gastos,  
**Para** no tener que clasificar manualmente cada gasto.

**Criterios de Aceptación**:

```
DADO que estoy logueado en la aplicación
Y voy a registrar un gasto con descripción "Cena en restaurante italiano"
Y dejo el campo de categoría vacío
CUANDO guardo el gasto
ENTONCES el sistema analizará la descripción
Y asignará automáticamente la categoría "Alimentación"
Y el gasto aparecerá en la lista con esta categoría
```

```
DADO que estoy logueado en la aplicación
Y voy a registrar un gasto con descripción "Netflix mensual"
Y dejo el campo de categoría vacío
CUANDO guardo el gasto
ENTONCES el sistema analizará la descripción
Y asignará automáticamente la categoría "Entretenimiento"
```

```
DADO que estoy logueado en la aplicación
Y voy a registrar un gasto con descripción "Varios"
Y dejo el campo de categoría vacío
CUANDO guardo el gasto
ENTONCES el sistema no encontrará coincidencia
Y asignará la categoría "Otros"
```

** Definition of Done**:
- [ ] Algoritmo de categorización implementado
- [ ] Mapeo de palabras clave funcional
- [ ] Categoría "Otros" para gastos no reconocibles
- [ ] Tests unitarios pasando con múltiples escenarios
- [ ] Documentación de palabras clave accesible

---

#### HU-06: Editar un Gasto Existente

**Como** usuario,  
**Quiero** poder editar los detalles de un gasto ya registrado,  
**Para** corregir errores o actualizar información.

**Criterios de Aceptación**:

```
DADO que tengo gastos registrados
Y accedo a la lista de gastos
Y selecciono un gasto específico
Y modifico la descripción a "Supermercado Día"
Y modifico el monto a 35.50
CUANDO confirmo los cambios
ENTONCES el gasto será actualizado exitosamente
Y la lista mostrará los nuevos valores
Y las estadísticas se recalcularán automáticamente
```

** Definition of Done**:
- [ ] Función de edición accesible desde la lista
- [ ] Campos editables con valores actuales
- [ ] Validación de campos al guardar
- [ ] Actualización en tiempo real de UI y estadísticas
- [ ] Tests unitarios pasando

---

#### HU-07: Eliminar un Gasto

**Como** usuario,  
**Quiero** poder eliminar un gasto que ya no deseo registrar,  
**Para** mantener limpia mi lista de gastos.

**Criterios de Aceptación**:

```
DADO que tengo gastos registrados
Y accedo a la lista de gastos
Y selecciono un gasto para eliminar
CUANDO confirmo la eliminación
ENTONCES el gasto será removido de la lista
Y las estadísticas se actualizarán automáticamente
Y veré un mensaje de confirmación
```

```
DADO que tengo gastos registrados
Y accedo a la lista de gastos
Y selecciono un gasto para eliminar
Y cancelo la confirmación de eliminación
ENTONCES el gasto permanecerá en la lista
Y no habrá ningún cambio
```

** Definition of Done**:
- [ ] Opción de eliminación visible en cada gasto
- [ ] Confirmación antes de eliminar
- [ ] Opción de cancelar la acción
- [ ] Actualización de UI y estadísticas tras eliminar
- [ ] Tests unitarios pasando

---

### 8.3 Épica 3: Visualización de Estadísticas

---

#### HU-08: Ver Resumen de Gastos Mensuales

**Como** usuario,  
**Quiero** ver un resumen de mis gastos mensuales,  
**Para** entender cuánto he gastado en el mes actual.

**Criterios de Aceptación**:

```
DADO que estoy logueado en la aplicación
Y tengo gastos registrados para el mes actual
CUANDO accedo a la sección "Estadísticas"
ENTONCES veré el total de gastos del mes
Y veré el número total de transacciones
Y veré el gasto promedio por transacción
Y veré la categoría con mayor gasto
```

```
DADO que estoy logueado en la aplicación
Y NO tengo gastos registrados para el mes actual
CUANDO accedo a la sección "Estadísticas"
ENTONCES veré un mensaje indicando "No hay gastos registrados este mes"
Y los gráficos mostrarán vacío o mensaje informativo
```

** Definition of Done**:
- [ ] Dashboard de estadísticas implementado
- [ ] Cálculos de métricas correctos
- [ ] Manejo de escenario sin datos
- [ ] Diseño visual limpio y profesional
- [ ] Tests unitarios pasando

---

#### HU-09: Ver Gráfico de Distribución por Categorías

**Como** usuario,  
**Quiero** ver un gráfico que muestre cómo se distribuyen mis gastos por categoría,  
**Para** identificar en qué áreas gasto más.

**Criterios de Aceptación**:

```
DADO que estoy logueado en la aplicación
Y tengo gastos en múltiples categorías
CUANDO accedo a la sección "Estadísticas"
ENTONCES veré un gráfico de pastel mostrando la distribución por categoría
Y cada segmento tendrá un color distinto
Y cada segmento mostrará el nombre de la categoría
Y el porcentaje o monto será visible al pasar el cursor
```

```
DADO que estoy logueado en la aplicación
Y todos mis gastos están en una sola categoría
CUANDO accedo a la sección "Estadísticas"
ENTONCES el gráfico de pastel mostrará 100% en esa categoría
Y habrá un mensaje indicando que solo hay una categoría
```

** Definition of Done**:
- [ ] Gráfico de pastel implementado con Gradio
- [ ] Colores diferenciados por categoría
- [ ] Tooltips con información detallada
- [ ] Actualización en tiempo real con cambios en datos
- [ ] Tests unitarios pasando

---

#### HU-10: Filtrar Estadísticas por Período

**Como** usuario,  
**Quiero** poder seleccionar el mes y año que deseo visualizar,  
**Para** comparar gastos entre diferentes períodos.

**Criterios de Aceptación**:

```
DADO que estoy logueado en la aplicación
Y tengo gastos en diferentes meses
CUANDO selecciono "Enero 2025" en el selector de período
ENTONCES las estadísticas se actualizarán para mostrar solo gastos de ese mes
Y el gráfico de categorías mostrará los datos de ese período
```

```
DADO que estoy logueado en la aplicación
Y no hay gastos para el período seleccionado
CUANDO selecciono un mes sin gastos
ENTONCES veré un mensaje indicando la ausencia de datos
Y los gráficos mostrarán estado vacío
```

** Definition of Done**:
- [ ] Selector de mes/año funcional
- [ ] Filtrado correcto de datos por período
- [ ] Actualización de todos los componentes estadísticos
- [ ] Manejo graceful de períodos sin datos
- [ ] Tests unitarios pasando

---

### 8.4 Épica 4: Experiencia de Usuario

---

#### HU-11: Navegación Intuitiva entre Secciones

**Como** usuario,  
**Quiero** navegar fácilmente entre las diferentes secciones de la aplicación,  
**Para** gestionar mis gastos de manera eficiente.

**Criterios de Aceptación**:

```
DADO que estoy logueado en la aplicación
ENTONCES veré claramente las opciones de navegación
Y podré acceder a "Registrar Gasto" con un clic
Y podré acceder a "Ver Gastos" con un clic
Y podré acceder a "Estadísticas" con un clic
Y podré acceder a "Cerrar Sesión" con un clic
```

** Definition of Done**:
- [ ] Navegación clara y accesible
- [ ] Feedback visual del elemento activo
- [ ] Consistencia en la ubicación de elementos de navegación

---

#### HU-12: Mensajes de Feedback Claros

**Como** usuario,  
**Quiero** recibir mensajes claros cuando realice acciones,  
**Para** saber que mis acciones fueron procesadas correctamente.

**Criterios de Aceptación**:

```
DADO que he completado una acción exitosa (registrar, editar, eliminar gasto)
ENTONCES veré un mensaje de éxito en color verde
Y el mensaje describirá la acción realizada
Y el mensaje desaparecerá después de unos segundos
```

```
DADO que he cometido un error en el formulario
ENTONCES veré un mensaje de error específico
Y el mensaje indicará qué campo es incorrecto
Y el mensaje estará en color rojo
```

** Definition of Done**:
- [ ] Sistema de notificaciones implementado
- [ ] Colores diferenciados para éxito/error
- [ ] Mensajes descriptivos y útiles
- [ ] Auto-dismiss para mensajes de éxito

---

## 9. Criterios de Aceptación del Producto

### 9.1 ACEPT-01: Funcionalidad Completa

| # | Criterio | Método de Verificación |
|---|----------|------------------------|
| 1 | El usuario puede registrarse con datos válidos | Prueba manual: registro con datos nuevos |
| 2 | El usuario puede iniciar sesión con credenciales correctas | Prueba manual: login con usuario creado |
| 3 | El usuario recibe error con credenciales inválidas | Prueba manual: login con datos incorrectos |
| 4 | El usuario puede registrar un gasto con todos los campos | Prueba manual: completar formulario y guardar |
| 5 | El sistema categoriza automáticamente los gastos | Verificación: gastos con palabras clave deben tener categoría asignada |
| 6 | El usuario puede ver la lista de sus gastos | Prueba manual: navegar a sección de lista |
| 7 | El usuario puede editar un gasto existente | Prueba manual: modificar y guardar cambios |
| 8 | El usuario puede eliminar un gasto | Prueba manual: eliminar gasto y verificar removal |
| 9 | Las estadísticas muestran totales correctos | Verificación manual: comparar suma vs. mostrado |
| 10 | El gráfico de categorías se genera correctamente | Verificación visual: gráfico con datos correctos |

### 9.2 ACEPT-02: Validaciones

| # | Criterio | Comportamiento Esperado |
|---|----------|------------------------|
| 1 | Monto vacío o cero | Error: "El monto es obligatorio y debe ser mayor a 0" |
| 2 | Monto negativo | Error: "El monto debe ser un valor positivo" |
| 3 | Fecha futura | Error: "La fecha no puede ser futura" |
| 4 | Descripción vacía | Permitir (descripción no obligatoria) |
| 5 | Descripción muy larga (>200 chars) | Error: "La descripción no puede exceder 200 caracteres" |
| 6 | Login con usuario inexistente | Error: "El usuario no existe" |
| 7 | Login con contraseña incorrecta | Error: "Contraseña incorrecta" |
| 8 | Registro con usuario existente | Error: "El nombre de usuario ya está en uso" |
| 9 | Registro con contraseña corta (<4 chars) | Error: "La contraseña debe tener al menos 4 caracteres" |

### 9.3 ACEPT-03: Estados de UI

| Escenario | Estado Esperado |
|-----------|-----------------|
| Sin gastos registrados | Mensaje: "No tienes gastos registrados. ¡Comienza añadiendo tu primer gasto!" |
| Sin gastos en período seleccionado | Mensaje: "No hay gastos para el período seleccionado" |
| Todas las categorías vacías | Gráfico: mensaje o estado vacío |
| Categorización sin match | El gasto se muestra con categoría "Otros" |
| Éxito en operación | Toast/notification verde con mensaje de éxito |
| Error en operación | Toast/notification roja con mensaje de error |

---

## 10. Estructura del Proyecto

### 10.1 Arquitectura del Sistema

```
gastos_personales_prototype/
├── main.py                    # Punto de entrada de la aplicación
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Documentación del proyecto
├── config/
│   ├── __init__.py
│   └── categories.py         # Configuración de categorías y palabras clave
├── models/
│   ├── __init__.py
│   ├── user.py                # Modelo de Usuario
│   ├── expense.py             # Modelo de Gasto
│   └── category.py            # Modelo de Categoría
├── services/
│   ├── __init__.py
│   ├── auth_service.py        # Lógica de autenticación
│   ├── expense_service.py     # Lógica de negocio de gastos
│   ├── categorization_service.py  # Lógica de categorización automática
│   └── statistics_service.py  # Lógica de cálculos estadísticos
├── repositories/
│   ├── __init__.py
│   ├── user_repository.py     # Acceso a datos de usuarios (en memoria)
│   └── expense_repository.py  # Acceso a datos de gastos (en memoria)
├── ui/
│   ├── __init__.py
│   ├── auth_ui.py             # Interfaz de login/registro
│   ├── expense_ui.py          # Interfaz de gestión de gastos
│   ├── statistics_ui.py      # Interfaz de estadísticas
│   └── components.py         # Componentes reutilizables de UI
├── utils/
│   ├── __init__.py
│   ├── validators.py          # Funciones de validación
│   └── helpers.py             # Funciones auxiliares
└── tests/
    ├── __init__.py
    ├── test_auth_service.py
    ├── test_expense_service.py
    ├── test_categorization.py
    └── test_statistics.py
```

### 10.2 Diagrama de Flujo de Usuario

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐   │
│  │   LOGIN     │───►│  REGISTRO    │───►│  INTERFAZ       │   │
│  │   /REGISTRO │    │  (si nuevo)  │    │  PRINCIPAL      │   │
│  └─────────────┘    └──────────────┘    └────────┬────────┘   │
│                                                  │             │
│         ┌────────────────────────────────────────┼──────────┐ │
│         │                                        │          │ │
│         ▼                                        ▼          ▼ │
│  ┌──────────────┐                      ┌──────────────┐ ┌─────────┐
│  │   CERRAR     │                      │   REGISTRAR  │ │ VER     │
│  │   SESIÓN     │                      │   GASTO      │ │ GASTOS  │
│  └──────────────┘                      └──────┬───────┘ └────┬──┘
│                                                │              │
│                                                ▼              │
│                                        ┌──────────────┐        │
│                                        │ ESTADÍSTICAS │        │
│                                        │  Y GRÁFICOS  │        │
│                                        └──────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11. Especificaciones Técnicas Detalladas

### 11.1 Modelo de Datos

#### 11.1.1 Clase Usuario

```python
class User:
    def __init__(
        self,
        username: str,
        password: str,  # En prototipo sin hash real
        full_name: str
    ):
        self.username: str
        self.password: str
        self.full_name: str
        self.created_at: datetime
```

#### 11.1.2 Clase Gasto

```python
class Expense:
    def __init__(
        self,
        description: str,
        amount: float,
        date: datetime,
        category: str,
        user_id: str
    ):
        self.id: str  # UUID
        self.description: str
        self.amount: float
        self.date: datetime
        self.category: str
        self.user_id: str
        self.created_at: datetime
        self.updated_at: datetime
```

#### 11.1.3 Clase Categoría

```python
class Category:
    def __init__(
        self,
        name: str,
        icon: str,
        keywords: List[str]
    ):
        self.name: str
        self.icon: str
        self.keywords: List[str]
```

### 11.2 Estructura de Datos en Memoria

```python
# Almacenamiento en memoria (para prototipo)
users_db: Dict[str, User] = {}
expenses_db: List[Expense] = []
current_session: Optional[User] = None
```

### 11.3 API del Backend (Interfaces de Servicio)

#### 11.3.1 AuthService

```python
class AuthService:
    def register(self, username: str, password: str, full_name: str) -> Result[User]
    def login(self, username: str, password: str) -> Result[User]
    def logout(self) -> None
    def get_current_user(self) -> Optional[User]
    def is_authenticated(self) -> bool
```

#### 11.3.2 ExpenseService

```python
class ExpenseService:
    def create_expense(self, expense: Expense) -> Result[Expense]
    def update_expense(self, expense_id: str, updates: Dict) -> Result[Expense]
    def delete_expense(self, expense_id: str) -> Result[bool]
    def get_expenses(self, user_id: str, filters: Dict) -> List[Expense]
    def get_expense_by_id(self, expense_id: str) -> Optional[Expense]
```

#### 11.3.3 CategorizationService

```python
class CategorizationService:
    def categorize(self, description: str) -> Category
    def get_all_categories(self) -> List[Category]
    def get_category_by_name(self, name: str) -> Optional[Category]
```

#### 11.3.4 StatisticsService

```python
class StatisticsService:
    def get_total_expenses(self, user_id: str, period: Period) -> float
    def get_expenses_by_category(self, user_id: str, period: Period) -> Dict[str, float]
    def get_average_expense(self, user_id: str, period: Period) -> float
    def get_expense_count(self, user_id: str, period: Period) -> int
    def get_top_category(self, user_id: str, period: Period) -> Optional[Category]
    def get_monthly_comparison(self, user_id: str) -> Dict[str, Any]
```

---

## 12. Dependencias del Proyecto

### 12.1 requirements.txt

```
gradio>=4.0.0
matplotlib>=3.7.0
python-dateutil>=2.8.0
uuid>=1.30
typing-extensions>=4.0.0
```

### 12.2 Dependencias de Desarrollo (Opcional)

```
pytest>=7.0.0
pytest-cov>=4.0.0
```

---

## 13. Limitaciones del Prototipo

### 13.1 Limitaciones Conocidas

| Limitación | Impacto | Mitigation |
|------------|---------|------------|
| Sin persistencia de datos | Datos se pierden al reiniciar | Documentar como comportamiento esperado |
| Un solo usuario a la vez | No prueba multi-usuario | Arquitectura preparada para expansión |
| Sin base de datos real | Escalabilidad no probada | Estructura de repository permite migración |
| Autenticación simulada | Seguridad no implementada | Claramente documentado como prototipo |
| Sin pruebas de carga | Rendimiento bajo alta demanda | Código optimizado para operaciones simples |

### 13.2 Notas Importantes para el Cliente

> ⚠️ **IMPORTANTE**: Este es un prototipo funcional diseñado para demostración ejecutiva. Los datos ingresados durante la sesión se almacenan únicamente en memoria RAM y se perderán al cerrar/reiniciar la aplicación. No debe utilizarse para gestionar finanzas reales en esta etapa.

---

## 14. Roadmap de Funcionalidades Futuras

### 14.1 Fase 2: Versión con Persistencia (Post-Aprobación)

- [ ] Implementación de base de datos SQLite/PostgreSQL
- [ ] Sistema de autenticación con hashing de contraseñas
- [ ] CRUD completo de usuarios
- [ ] Persistencia de gastos entre sesiones

### 14.2 Fase 3: Versión Multi-Usuario

- [ ] Sistema de autenticación JWT
- [ ] Aislamiento de datos por usuario
- [ ] Perfiles de usuario personalizables
- [ ] Roles y permisos

### 14.3 Fase 4: Funcionalidades Avanzadas

- [ ] Exportación a PDF/Excel
- [ ] Presupuestos y alertas de límite
- [ ] Categorías personalizadas por usuario
- [ ] Integración con APIs bancarias
- [ ] Aplicación móvil nativa
- [ ] Análisis predictivo de gastos

---

## 15. Glosario de Términos

| Término | Definición |
|---------|------------|
| **Prototipo** | Versión inicial de un producto con funcionalidad limitada para demostración |
| **Core/Feature** | Clasificación de requerimientos: Core = esencial, Feature = adicional |
| **CRUD** | Create, Read, Update, Delete - operaciones básicas de gestión de datos |
| **En memoria** | Almacenamiento temporal en RAM, no persistente |
| **Categorización automática** | Proceso de clasificar gastos usando palabras clave sin intervención del usuario |
| **Dashboard** | Panel de control con métricas y visualizaciones |
| **Gradio** | Framework de Python para crear interfaces web de machine learning |
| **POC** | Proof of Concept - demostración de viabilidad técnica |

---

## 16. Aprobaciones

| Rol | Nombre | Fecha | Firma |
|-----|--------|-------|-------|
| Scrum Master | [TBD] | [Fecha] | ____________ |
| Product Owner | [TBD] | [Fecha] | ____________ |
| Equipo de Desarrollo | [TBD] | [Fecha] | ____________ |
| Cliente/Stakeholder | [TBD] | [Fecha] | ____________ |

---

## 17. Historial de Versiones

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | Enero 2025 | Scrum Master | Versión inicial del documento |

---

*Este documento es la única fuente de verdad para los requerimientos del proyecto. Todo el equipo de desarrollo debe referirse a este documento para asegurar que el producto cumpla con las expectativas del cliente.*