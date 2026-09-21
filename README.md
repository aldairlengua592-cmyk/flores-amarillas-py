# Flores amarillas · Streamlit

Versión independiente de la página original. `app.py` contiene el HTML, CSS y JavaScript que Streamlit presenta en el navegador. No necesita leer la carpeta `regalo-flores`.

## Ejecutar

Desde una terminal en esta carpeta:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abre la dirección que muestra la terminal (normalmente http://localhost:8501). Para detener el servidor, pulsa Ctrl+C. Un archivo Streamlit se ejecuta con este comando, no abriéndolo con doble clic.

## Archivos

- `app.py`: aplicación completa con interfaz y animaciones integradas.
- `cancion.mp3`: copia del audio original, incrustado por Python al servir la página.
- `requirements.txt`: versión de Streamlit utilizada.

## Personalización

Edita al inicio de `app.py`: `NOMBRE`, `MENSAJE`, `NOMBRE_CANCION`, `FRASE_INICIAL`, `COLOR_PRINCIPAL`, `VOLUMEN` y `ARCHIVO_AUDIO`.

El volumen está al 5 % y la canción se repite en bucle. Comienza al pulsar «Descubrir mi regalo»; si el navegador impide el inicio, pulsa «Reproducir». El volumen del dispositivo también influye en el sonido.

Conserva los pétalos amarillos, estrellas blancas, flores animadas y corazones al tocar el ramo. La interfaz se adapta al ancho de pantalla y permite desplazarse verticalmente en celulares.

Implementado con [st.html de Streamlit](https://docs.streamlit.io/1.57.0/develop/api-reference/text/st.html), habilitando JavaScript para la interfaz local.
