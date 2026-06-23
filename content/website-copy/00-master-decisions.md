# Decisiones maestras del sitio — ALMAVIVA

## Estado del prototipo
Rama: `prototype/almaviva-program-pages`
Estado: borrador para revisión de Ana — no publicar en producción.

## Arquitectura aprobada

```
/                       Homepage
/programas.html         Hub de decisión (los cuatro caminos)
/sesiones-individuales.html
/conecta.html
/foco.html
/intensivo.html
/sobre-ana.html         Placeholder expandible
/contacto.html          Datos de contacto verificados
/privacidad.html        Placeholder legal — REQUIERE REVISIÓN
```

## Principio rector
"La web explica. El PDF profundiza."
La visita debe entender ALMAVIVA, los cuatro caminos y el siguiente paso SIN abrir un PDF.
Los PDFs son capa de detalle, no CTA principal.

## Decisiones tomadas

| Decisión | Estado | Notas |
|----------|--------|-------|
| Arquitectura multi-página | Aprobada | 4 páginas de programa + hub + soporte |
| CTA principal | Aprobada | "Agendar conversación inicial" → WhatsApp |
| Nombre programas | En revisión | "Sesiones Individuales" vs "Sesiones y Packs" |
| Testimonios | Diferidos | No en prototipo; necesitan permiso real |
| Precios | No publicar | Gestionar en conversación hasta decisión |
| Límite terapéutico | Incluir | Texto canónico aprobado en shared/ |
| PDFs como CTAs secundarias | Aprobado | Después del contenido web, no como primera opción |

## Decisiones pendientes

Ver `shared/open-questions-for-ana.md` para lista completa.

Críticas antes del lanzamiento:
1. Precios y moneda
2. Mecánica de Conecta (cohortes vs. inscripción continua)
3. Política de privacidad (jurisdicción + redacción legal)
4. Herramienta de contacto/agenda
5. Testimonios reales con permiso
