# ALMAVIVA — Hoja de decisión: ritmo visual compartido (Fase 2C)

*Para: Ana Carolina · Preparado: 6 de julio de 2026*

Este documento es para que tú decidas. No se ha cambiado nada todavía: cada
punto de la sección 6 espera tu aprobación (o tu rechazo) antes de que se
toque una sola línea del sitio.

---

## 1. Resumen ejecutivo

Tu sitio hoy funciona bien página por página. Cada página se ve como la
aprobaste: Inicio, Foco, Intensivo, Sesiones Individuales y Sobre mí están
completas, rápidas y fieles a sus diseños originales.

Lo que falta no es arreglar páginas rotas — no hay ninguna rota. Lo que falta
es **ritmo compartido**: cuando pasas de Inicio a Foco, o de Foco a Sesiones,
los márgenes laterales y el ancho del contenido cambian de una página a otra.
Cada página conserva el sistema de su diseño original aprobado, y esos
sistemas no coinciden entre sí.

De las cinco páginas, **Inicio tiene el ritmo más equilibrado**: un ancho de
contenido cómodo, márgenes generosos y consistentes, y una primera pantalla
que muestra lo esencial sin apretar nada.

La recomendación es simple: **usar Inicio como referencia compartida** y
alinear las otras cuatro páginas a su ritmo. Esto es alineación, no rediseño —
los textos, colores, fotos, tipografías y el orden de las secciones no cambian.

Necesitamos tu aprobación porque las cuatro subpáginas ya fueron aprobadas
visualmente tal como están, y este cambio las modificaría a propósito.
**Inicio no se toca: queda exactamente igual.**

## 2. Qué observó la revisión externa

Pedimos una revisión externa de márgenes y de la primera pantalla a varios
asistentes de IA. Usamos **Claude.ai como ancla principal** de la
recomendación; Gemini y Grok revisaron también y apoyaron la dirección
general, aunque no definieron el plan de ejecución.

El punto donde más coincidieron es este: **alinear el sitio al ritmo de
Inicio, mantener excepciones donde sirven al diseño, y evitar una
uniformidad mecánica** (no forzar que todo mida exactamente lo mismo si un
elemento — como el hero ancho de Foco — cumple un rol visual propio).

No fue una decisión unánime en cada detalle; donde hubo diferencias de
criterio, prevaleció el ancla principal y el sentido común de tu marca.

## 3. Qué se mantiene igual

- **Inicio / index.html: sin cambios.** Sigue siendo la referencia.
- Los **textos** no cambian — ni una palabra.
- Los **colores** no cambian.
- El **estilo tipográfico** no cambia.
- El **orden de las secciones** no cambia.
- Las **imágenes** no cambian, con una sola excepción: la foto del hero de
  Sobre mí en celular, que hoy aparece diminuta por un defecto técnico
  (ver punto 4 de la sección 6).
- Los **anchos internos de texto** se preservan: los párrafos no se vuelven
  líneas kilométricas de borde a borde.
- **Sobre mí sigue siendo editorial y biográfica**, una página de confianza,
  no de venta. No se le agrega ningún botón forzado en la primera pantalla.
- **Foco puede conservar su hero ancho** como acento propio de la página,
  documentado como excepción (esa decisión es tuya — sección 6, punto 6).

## 4. Ritmo global propuesto

El ritmo de Inicio, aplicado a todo el sitio:

- **Ancho máximo del contenido (escritorio):** 1120 px
- **Margen lateral (escritorio):** 32 px
- **Margen lateral (celular):** 22 px
- Los anchos internos de texto se preservan (los bloques de lectura siguen
  siendo angostos e íntimos donde corresponde).
- Se permiten **excepciones documentadas** solo para imágenes/heros que
  sirven a la página — no como regla general.

¿Qué gana el sitio con esto? Coherencia: al navegar de una página a otra,
todo respira igual. El resultado se siente más calmado, más premium y más
"de una sola pieza" — sin perder la personalidad de cada página.

## 5. Evidencia de medidas

Medimos las cinco páginas en cuatro tamaños de pantalla. Los sistemas
actuales, en escritorio:

| Página | Sistema actual | Comparado con Inicio |
|---|---|---|
| **Inicio** (referencia) | 1120 px + margen 32 px (22 px en celular) | — |
| Foco | Cuerpo a 1180 px + hero más ancho (1290 px) | Contenido más ancho, márgenes distintos |
| Intensivo | 1140 px | Casi igual — diferencia pequeña |
| Sesiones Individuales | 980 px | Notablemente más angosta que el resto |
| Sobre mí | 1180 px con margen "elástico" | Más ancha, y el margen varía con la ventana |

En palabras simples: **cada página es coherente consigo misma, pero el sitio
todavía no es coherente como conjunto.**

Sobre la primera pantalla (lo que se ve sin hacer scroll, en un monitor
típico de escritorio):

- **Inicio está perfecta**: título, foto, botones visibles, y se alcanza a
  ver el inicio de la sección siguiente — una invitación natural a seguir
  bajando.
- **Foco es la única con un problema real**: su hero es tan alto que el botón
  "Agendar sesión de descubrimiento" apenas entra en pantalla y no se ve
  ninguna pista de que hay más contenido abajo.
- **Sobre mí no tiene botón en la primera pantalla**, y eso está bien para su
  rol: es una página para conocerte, no para vender.
- Intensivo y Sesiones están en buen rango.

## 6. Decisiones que necesito que apruebes

1. **Aprobar Inicio como ritmo compartido** — 1120 px de ancho / 32 px de
   margen en escritorio / 22 px en celular.

2. **Aprobar la alineación de Intensivo** — es una corrección horizontal
   pequeña (su ancho ya es casi igual al de Inicio). Riesgo visual bajo.

3. **Aprobar la alineación de Sobre mí** — reemplazar su margen "elástico"
   por el ritmo fijo de Inicio, manteniendo su pausa editorial. Sin botón
   forzado en la primera pantalla.

4. **Aprobar la corrección de la foto móvil de Sobre mí** — hoy, en celular,
   la foto principal aparece reducida a un punto diminuto por un defecto
   heredado del diseño original. Se corrige como defecto de producción, no
   como rediseño: la foto simplemente volverá a verse en celular.

5. **Aprobar la alineación del cuerpo de Foco** — las secciones de contenido
   se alinean al ritmo de Inicio, preservando los anchos internos de texto.

6. **Decidir el hero de Foco** (elige una):
   - **Opción A — recomendada:** mantener el hero ancho con su foto grande,
     como excepción documentada y acento propio de la página.
   - **Opción B:** reducir el ancho del hero hacia el ritmo global, para una
     uniformidad más estricta.

7. **Aprobar la corrección de altura del hero de Foco** — reducir su presión
   vertical para que el botón se vea con claridad y aparezca una pista de la
   siguiente sección en pantallas de escritorio. Los textos no cambian.

8. **Aprobar la ampliación de Sesiones Individuales** — ensanchar su marco
   exterior hacia el ritmo de Inicio, preservando sus bloques de texto
   angostos para que no pierda su carácter íntimo.

## 7. Orden recomendado de implementación

Un cambio por vez, una página por commit, con tu revisión entre medio:

1. **Intensivo** — piloto de alineación
2. **Sobre mí** — alineación de márgenes
3. **Sobre mí** — corrección de la foto móvil
4. **Foco** — alineación del cuerpo
5. **Foco** — corrección de altura del hero
6. **Sesiones** — ampliación del marco

¿Por qué este orden?

- **Intensivo va primero** porque es el cambio más pequeño y de menor riesgo:
  sirve para probar el sistema compartido en el caso más simple.
- **Foco no va primero** porque es la única página con un cambio vertical
  real (el fold), además del horizontal — mejor abordarla con el sistema ya
  probado.
- **Sesiones va al final** porque es el cambio horizontal más grande
  (980 → 1120 px): los textos se reacomodan más que en ninguna otra página y
  merece la revisión más tranquila.

## 8. Tabla de riesgos

| Página | Cambio propuesto | Riesgo | ¿Necesita tu aprobación? | Notas |
|---|---|---|---|---|
| index.html | Sin cambios | Ninguno | No | Sigue siendo la referencia. |
| intensivo.html | Alinear marco | Bajo | Sí | Mejor piloto técnico. |
| sobre-ana.html | Alinear margen + corregir foto móvil | Bajo-medio | Sí | Mantener tono editorial. |
| foco.html | Alinear cuerpo + corregir fold | Medio-alto | Sí | Mantener hero ancho como excepción recomendada. |
| sesiones-individuales.html | Ampliar marco | Medio-alto | Sí | Preservar bloques internos para no perder intimidad. |

## 9. Cómo se verificará cada cambio

Cada página, antes de dar por cerrado su cambio, pasa por las mismas puertas:

- Capturas de pantalla de antes y después.
- Revisión en cuatro tamaños: 1920, 1366, 390 y 375 px.
- Verificación de la primera pantalla en escritorio (1920×1001).
- Mediciones exactas de posición y tamaño de cada bloque.
- Comparación pixel a pixel de página completa donde aporte.
- Verificación de que los textos quedaron idénticos.
- Revisión de todos los enlaces.
- Revisión técnica de consola y red (sin errores).
- Y lo más importante: **tu visto bueno antes de pasar a la siguiente página
  de mayor riesgo.**

## 10. Recomendación final

- Aprobar **Inicio como ritmo compartido** del sitio.
- Aprobar la **armonización página por página** antes del control de calidad
  final.
- Mantener el **hero ancho de Foco** como la única excepción visual
  documentada.
- Corregir la **altura del hero de Foco** para liberar la primera pantalla.
- Corregir la **foto móvil de Sobre mí**.
- Partir con **Intensivo como piloto**.

El siguiente paso de ingeniería ocurre **solo después de que apruebes esta
hoja** — nada se implementa antes.

## 11. Checklist de aprobación para Ana

Marca lo que apruebas:

- [ ] Apruebo usar Inicio como ritmo visual compartido.
- [ ] Apruebo el estándar 1120 px / 32 px / 22 px.
- [ ] Apruebo preservar los anchos internos de texto.
- [ ] Apruebo alinear Intensivo.
- [ ] Apruebo alinear Sobre mí sin convertirla en una página más vendedora.
- [ ] Apruebo corregir la imagen móvil de Sobre mí.
- [ ] Apruebo alinear el cuerpo de Foco.
- [ ] Apruebo mantener el hero ancho de Foco como excepción documentada.
- [ ] Apruebo corregir la altura/fold de Foco.
- [ ] Apruebo ampliar Sesiones preservando su intimidad.
- [ ] Apruebo implementación página por página, con revisión antes de avanzar.

---

## Evidencia disponible

Medidas completas y contexto técnico:
`docs/verification/council/COUNCIL-BRIEF.md`

Capturas de la primera pantalla (escritorio 1920 px, y celular para Inicio):

- `docs/verification/council/index-1920-fold.png`
- `docs/verification/council/foco-1920-fold.png`
- `docs/verification/council/intensivo-1920-fold.png`
- `docs/verification/council/sesiones-1920-fold.png`
- `docs/verification/council/sobre-ana-1920-fold.png`
- `docs/verification/council/index-390-fold.png`
- Página completa de Inicio: `docs/verification/council/index-1920-fullpage.png`
  y `docs/verification/council/index-390-fullpage.png`

*Nota técnica: esa carpeta de evidencia es local (no viaja con el historial
del repositorio), así que las capturas se comparten aparte si hace falta.*
