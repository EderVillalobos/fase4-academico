# Analisis completo de la Guia y el Anexo 3 - Fase 4

## Observacion previa

Este espacio es independiente y esta dedicado solo al trabajo academico de la Fase 4.

## 1. Anexo 3 - Problema a desarrollar Fase 4

### Pagina 1

- Presenta el contexto general del ejercicio.
- El proyecto asignado es un **sistema integral orientado a objetos** para la empresa **Software FJ**.
- El sistema debe gestionar:
  - clientes
  - servicios
  - reservas
- El dominio del problema incluye varios tipos de servicios:
  - reservas de salas
  - alquiler de equipos
  - asesorias especializadas
- Exige una aplicacion:
  - estable
  - modular
  - extensible
- Obliga a aplicar principios de POO:
  - abstraccion
  - herencia
  - polimorfismo
  - encapsulacion
  - manejo avanzado de excepciones
- Indica explicitamente que:
  - no se debe usar base de datos
  - la informacion se gestiona con objetos y listas
  - el unico uso de archivos es para logs de eventos y errores

### Pagina 2

- Profundiza en el requisito de manejo de excepciones.
- Deben usarse:
  - `try/except`
  - `try/except/else`
  - `try/except/finally`
  - encadenamiento de excepciones
- Cada error detectado debe registrarse en un archivo de logs.
- La aplicacion debe continuar activa aun cuando ocurra un error.
- Enumera las piezas minimas de la arquitectura:
  - una clase abstracta para entidades generales
  - una clase `Cliente` con validaciones robustas
  - una clase abstracta `Servicio`
  - al menos tres servicios especializados
  - una clase `Reserva` que integre cliente, servicio, duracion y estado
- La clase `Reserva` debe soportar:
  - confirmacion
  - cancelacion
  - procesamiento
  - control de excepciones
- Se piden metodos sobrecargados, por ejemplo para calcular costos con:
  - impuestos
  - descuentos
  - parametros opcionales

### Pagina 3

- Reitera que debe existir un archivo de logs con errores y eventos relevantes.
- El sistema debe simular al menos **10 operaciones completas**.
- Las operaciones deben incluir:
  - registros validos e invalidos de clientes
  - creacion correcta e incorrecta de servicios
  - reservas exitosas y fallidas
- El objetivo es demostrar que el programa sigue funcionando ante errores graves.
- Se debe entregar un proyecto:
  - funcional
  - organizado
  - documentado
  - ejecutable sin interrupciones
- El enfoque sigue siendo la correcta aplicacion de POO y excepciones en un entorno sin base de datos.

## 2. Guia para el desarrollo del componente practico - Fase 4

### Pagina 1

- Identifica la actividad como parte del curso de Programacion 213023.
- Define el marco general:
  - estrategia metodologica: aprendizaje basado en problemas
  - tipologia: metodologico
  - momento: intermedio
  - puntaje: 150
  - actividad simulada
- El resultado de aprendizaje esperado es:
  - implementar manejo de excepciones en aplicaciones orientadas a objetos
  - buscar estabilidad y robustez
  - gestionar errores de forma adecuada

### Pagina 2

- Indica que el ejercicio debe desarrollarse dentro de GitHub.
- La entrega se comparte mediante el enlace del repositorio.
- Fija el contexto de la actividad:
  - escenario simulado con apoyo TIC
  - actividad colaborativa
  - numero de actividad 4
  - inicia el 9 de junio de 2026
  - finaliza el 6 de julio de 2026
- Lista recursos de apoyo bibliografico y enlaces sobre:
  - errores en Python
  - programacion orientada a objetos
  - uso de GitHub

### Pagina 3

- Vincula la actividad con el Anexo 3.
- Pide que cada grupo desarrolle actividades para garantizar:
  - estabilidad
  - robustez
  - adecuado manejo de errores
- Cada estudiante debe:
  - entrar al repositorio del grupo en GitHub
  - implementar o continuar codigo
  - documentar claramente el codigo
  - ejecutar secuencialmente el codigo
  - corregir fallos detectados
- La participacion de todos los integrantes es obligatoria.
- La evidencia grupal a entregar es un **PDF** con:
  - portada
  - introduccion
  - enlace al repositorio de GitHub
  - conclusiones
  - referencias APA

### Pagina 4

- Da lineamientos generales para la elaboracion de evidencias.
- Recomienda revisar:
  - noticias del curso
  - encuentros sincronos
  - invitaciones de CIPAS virtuales
- Exige:
  - ortografia correcta
  - normas de presentacion
  - normas de referenciacion
  - evitar plagio
- Sugiere revisar los productos con Turnitin.
- Incluye una advertencia sobre faltas academicas y sanciones.

### Pagina 5

- Detalla sanciones por fraude academico y plagio:
  - calificacion de cero
  - posible sancion disciplinaria
- Refuerza la necesidad de autoria propia y referencias correctas.

## 3. Que se requiere realmente para su desarrollo

### Requisitos funcionales

- Sistema sin base de datos.
- Gestion de:
  - clientes
  - servicios
  - reservas
- Al menos tres servicios especializados.
- Control de estado de reservas.
- Operaciones validas e invalidas para probar robustez.
- Registro de logs de errores y eventos.

### Requisitos tecnicos

- Programacion orientada a objetos.
- Uso de clases abstractas.
- Herencia y polimorfismo.
- Encapsulacion.
- Manejo robusto de excepciones.
- Uso de listas o estructuras en memoria.
- Persistencia solo para logs.

### Requisitos de validacion

- Validar datos obligatorios.
- Mantener la aplicacion activa ante errores.
- Registrar cada fallo con trazabilidad.
- Simular al menos 10 escenarios completos.

### Requisitos de entrega

- Proyecto unico funcional.
- Repositorio GitHub.
- Documento PDF con:
  - portada
  - introduccion
  - enlace del repositorio
  - conclusiones
  - referencias APA

## 4. Lectura tecnica para desarrollo

- El reto no pide una interfaz compleja, sino un sistema robusto y demostrable.
- La prioridad es validar el manejo de errores y la estabilidad del flujo.
- Debe quedar claro el ciclo:
  - crear cliente
  - crear servicio
  - generar reserva
  - confirmar o rechazar
  - registrar log
  - continuar ejecucion

## 5. Nota importante para el contexto actual

- Los documentos analizados describen un proyecto de **Python orientado a objetos sin base de datos**.
- Este espacio queda separado de cualquier otro proyecto tecnico.
- Si luego necesitas que lo convierta en una implementacion concreta, el siguiente paso es definir la estructura de clases, simulacion de datos y flujo de ejecucion.
