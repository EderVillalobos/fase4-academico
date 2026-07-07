# Fase 4 Ejercicio 1: Sistema Integral de Gestion de Clientes, Servicios y Reservas

Sistema integral orientado a objetos, sin uso de bases de datos, para gestionar clientes, servicios y reservas de Software FJ, una empresa que ofrece:

- reservas de salas
- alquiler de equipos
- asesorias especializadas

## Objetivo

Construir una aplicacion estable, modular y extensible que implemente de forma rigurosa:

- abstraccion
- herencia
- polimorfismo
- encapsulacion
- manejo avanzado de excepciones

El sistema debe seguir funcionando aun cuando se presenten errores durante su ejecucion. Toda la gestion se realiza mediante objetos, listas internas y archivos de registro para eventos y errores.

## Requisitos funcionales

- Clase abstracta para entidades generales del sistema.
- Clase `Cliente` con validaciones robustas y encapsulacion de datos personales.
- Clase abstracta `Servicio` y al menos tres servicios especializados con polimorfismo y metodos sobrescritos.
- Clase `Reserva` que integre cliente, servicio, duracion y estado.
- Metodos sobrecargados para calculo de costos con impuestos, descuentos o parametros opcionales.
- Archivo de logs para registrar errores y eventos relevantes.
- Simulacion de al menos 10 operaciones completas, incluyendo casos validos e invalidos.

## Manejo de errores

El sistema incorpora:

- excepciones personalizadas
- bloques `try/except`
- bloques `try/except/else`
- bloques `try/except/finally`
- encadenamiento de excepciones

Cada error detectado debe registrarse en el archivo de logs, manteniendo la aplicacion activa y estable en todo momento.

## Alcance

El sistema debe manejar errores provenientes de:

- datos invalidos
- parametros faltantes
- operaciones no permitidas
- intentos de reserva incorrectos
- servicios no disponibles
- calculos inconsistentes
- cualquier otra situacion que comprometa la operacion normal

## Estructura

- `src/` codigo fuente principal.
- `README.md` guia minima de ejecucion.
- `.gitignore` exclusiones locales.

## Ejecucion

```bash
python -m src.main
```

El flujo actual ejecuta la demostracion del sistema y genera los archivos de salida necesarios de forma local.
