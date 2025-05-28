# Proyecto JF Music

Este proyecto es una aplicación web para gestionar usuarios y canciones, con autenticación y privilegios de administrador. Permite el registro, inicio de sesión, visualización de canciones y, para administradores, la gestión de usuarios.

---

## Estructura del Proyecto

- **index.html**: Página principal. Muestra la lista de canciones a cualquier usuario autenticado (usuario normal o administrador). Incluye botón de cerrar sesión y, si el usuario es administrador, acceso al panel de administración.
- **login.html**: Página de inicio de sesión. Permite iniciar sesión o, si el usuario no existe, registrarse automáticamente desde el mismo formulario. También incluye enlace a la página de registro tradicional.
- **register.html**: Página de registro manual. Permite crear una nueva cuenta de usuario.
- **home.html**: Panel de administración. Solo accesible para usuarios cuyo correo termina en `@admin.com`. Muestra la lista de usuarios y la lista de canciones. Incluye botón de cerrar sesión.
- **/imagenes/**: Carpeta de imágenes (por ejemplo, el logo).
- **(Backend necesario)**: La API debe estar corriendo en `http://127.0.0.1:5000/api`.

---

## Instrucciones para Ejecutar la Aplicación

1. Asegúrate de tener el backend (API Flask) corriendo en `http://127.0.0.1:5000/api`.
2. Abre `index.html` en tu navegador para acceder a la lista de canciones (requiere inicio de sesión).
3. Abre `login.html` para iniciar sesión o crear un usuario automáticamente si no existe.
4. Si eres administrador (correo termina en `@admin.com`), tendrás acceso al panel de administración (`home.html`) desde el botón correspondiente en `index.html` o accediendo directamente.
5. Para registro manual, abre `register.html`.

---

## Requisitos

- Navegador web moderno.
- Backend Flask corriendo y accesible en `http://127.0.0.1:5000/api`.
- Conexión a Internet para cargar fuentes y estilos externos.

---

## Funcionalidades

- **Inicio de sesión y registro automático**: Si el usuario no existe al intentar iniciar sesión, puede registrarse directamente desde el mismo formulario.
- **Registro manual**: Disponible en `register.html`.
- **Lista de canciones**: Visible para todos los usuarios autenticados.
- **Panel de administración**: Solo para administradores, muestra usuarios y canciones.
- **Cierre de sesión**: Disponible en todas las páginas protegidas.
- **Protección de rutas**: Solo usuarios autenticados pueden acceder a las páginas principales; solo administradores pueden acceder al panel de administración.

---

## Notas

- Asegúrate de que la API esté corriendo antes de intentar cargar usuarios o canciones desde la aplicación.
- Puedes personalizar los estilos y la funcionalidad según tus necesidades.
- Si deseas agregar soporte para archivos de música reales, deberás modificar tanto el backend como el frontend para permitir la subida y reproducción de archivos de audio.
