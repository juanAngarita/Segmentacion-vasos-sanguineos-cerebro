# Segmentación de vasos sanguíneos del cerebro

Este proyecto fue desarrollado para la clase de análisis de imágenes médicas de la Maestría de Sistemas y computación de la Pontificia Universidad Javeriana. El objetivo del proyecto del proyecto era poder desarrollar un pipeline a partir del cuál se pudiera segmentar los vasos intracraneales del cerebro, a partir de tomografías con contraste. 

Tecnologías: python, ITK, matplotlib

# Contexto
En el ambito de las cirugías intracraneales es esencial la identificación de las estructuras vasculares y en partícular las venas corticales, que por tener paredes más delgadas que las arterias y por estar cercanas al hueso, son propensas a ser lesionadas durante el proceso de perforación del cráneo.

# Problemas/soluciones actuales.
En el contexto de fidelidad de la anatomía vascular, el examen preferible sería la arteriografía cerebral con sustracción digital; sin embargo, es una técnica invasiva y requiere recursos y equipamientos adicionales. Como alternativa, se emplea la angiotomografía, que implica la realización de este examen antes de la cirugía, lo cual requiere una dosis extra de medio de contraste y recursos adicionales. Un tercer camino es la realización de la segmentación de vasos intracraneales a partir de la resonancia con protocolo HARNESS (Harmonized Neuroimaging of Epilepsy Structural Sequences); sin embargo, es difícil la separación de los vasos corticales, especialmente de los senos durales del hueso. Además, presenta una distorsión del espacio tridimensional que resulta subóptima en el contexto de la cirugía estereotáctica, la cual requiere exactitud cartesiana.

# Objetivo
Realizar la segmentación de los vasos sanguíneos del cerebro usando únicamente UNA tomografía con contraste. 

## Entrada
Las imágenes 3D de entrada son tomografías con contraste de los pacientes.

<img width="672" height="298" alt="image" src="https://github.com/user-attachments/assets/db5d692d-892a-4095-becc-87b208e1692f" />

## Salida 
Imagen médica con la segmentación de los vasos sanguineos.

https://github.com/user-attachments/assets/7382c37c-f53c-46ea-998a-356ef7630aa7


