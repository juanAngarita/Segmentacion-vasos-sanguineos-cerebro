import itk
from sys import argv, stderr, exit
import matplotlib.pyplot as plt

Dimension = 3
PixelType = itk.F

OutputPixelType = itk.F
# .\proyecto.py .\TC_CONTRASTE_3.nii.gz .\TC_CONTRASTE_FINAL5500_3.nii.gz 284 184 97 1.0 -7.0 8.0 250 250
# -------------------------------------------------------------------------
if len(argv) < 10 :
  print("Usage: " , argv[0], " <InputImage> <OutputImage> <seedPositionX> <seedPositionY> <seedPositionZ> <sigma> <alpha> <beta> <timeThreshold> <stoppingTime>" )
  exit( )
# Obtener nombres de archivo de entrada y salida de la línea de comandos  
InputImage = argv[1]
OutputImage = argv[2]
# Definir el tipo de imagen
ImageType = itk.Image[PixelType, Dimension]
OutputImageType = itk.Image[ OutputPixelType, Dimension ]

# Crear un lector de archivos de imagen
ReaderType = itk.ImageFileReader[ImageType]
reader = ReaderType.New()
reader.SetFileName(InputImage)
reader.Update()

#1. Filtro de manejo de intensidad
IntensityWindowingImageFilterType = itk.IntensityWindowingImageFilter[ImageType, ImageType]
intensityFilter = IntensityWindowingImageFilterType.New()
intensityFilter.SetInput(reader.GetOutput())
intensityFilter.SetWindowMinimum(0)
intensityFilter.SetWindowMaximum(100)
intensityFilter.SetOutputMinimum(0)
intensityFilter.SetOutputMaximum(10000)

intensityFilter2 = IntensityWindowingImageFilterType.New()
intensityFilter2.SetInput(reader.GetOutput())
intensityFilter2.SetWindowMinimum(0)
intensityFilter2.SetWindowMaximum(100)
intensityFilter2.SetOutputMinimum(0)
intensityFilter2.SetOutputMaximum(10000)



#2. LEVEL SET
thresholder = itk.BinaryThresholdImageFilter[ ImageType, OutputImageType ].New()

timeThreshold = float( argv[9] )
thresholder.SetLowerThreshold( 0.0 )
thresholder.SetUpperThreshold( timeThreshold  )

thresholder.SetOutsideValue(  0  )
thresholder.SetInsideValue(  10000 )


CastFilterType = itk.RescaleIntensityImageFilter[
                            ImageType,
                            OutputImageType ]

#SMOOTHING FILTER
SmoothingFilterType = itk.CurvatureAnisotropicDiffusionImageFilter[
                            ImageType,
                            ImageType ]

smoothing = SmoothingFilterType.New()

smoothing.SetTimeStep( 0.125 )
smoothing.SetNumberOfIterations(  5 )
smoothing.SetConductanceParameter( 9.0 )

GradientFilterType = itk.GradientMagnitudeRecursiveGaussianImageFilter[
                            ImageType,
                            ImageType ]

SigmoidFilterType = itk.SigmoidImageFilter[
                            ImageType,
                            ImageType ]

#GRADIENT MAGNITUDE
gradientMagnitude = GradientFilterType.New()
sigma = float( argv[6] )
gradientMagnitude.SetSigma(  sigma  )

sigmoid = SigmoidFilterType.New()

sigmoid.SetOutputMinimum(  0.0  )
sigmoid.SetOutputMaximum(  1.0  )

FastMarchingFilterType = itk.FastMarchingImageFilter[ ImageType,
                            ImageType ]

fastMarching = FastMarchingFilterType.New()




alpha =  float( argv[7] )
beta  =  float( argv[8] )

sigmoid.SetAlpha( alpha )
sigmoid.SetBeta(  beta  )

NodeType = itk.LevelSetNode[PixelType, Dimension]
NodeContainer = itk.VectorContainer[itk.UI, NodeType]
seeds = NodeContainer.New()

seedPosition = [int( argv[3] ), int( argv[4] ), int( argv[5] )]


node = NodeType()
seedValue = 0.0

node.SetValue( seedValue )
node.SetIndex( seedPosition )

seeds.Initialize()
seeds.InsertElement( 0, node )

fastMarching.SetTrialPoints(  seeds  )

fastMarching.SetOutputSize(
        reader.GetOutput().GetBufferedRegion().GetSize() )

stoppingTime = float( argv[10] )

fastMarching.SetStoppingValue(  stoppingTime  )

smoothing.SetInput( reader.GetOutput() )
gradientMagnitude.SetInput( smoothing.GetOutput() )
sigmoid.SetInput( gradientMagnitude.GetOutput() )
fastMarching.SetInput( sigmoid.GetOutput() )
thresholder.SetInput( fastMarching.GetOutput() )

#2.1 rellenar espacions de la mascara
medianFilter = itk.MedianImageFilter[ImageType, ImageType].New()
medianFilter.SetInput(thresholder.GetOutput())
medianFilter.SetRadius(5)


#3. Segmentación arterias
FilterType = itk.ConnectedThresholdImageFilter[ImageType, ImageType]
connectedThreshold = FilterType.New()
connectedThreshold.SetLower(4800)
connectedThreshold.SetUpper(10000)
connectedThreshold.SetReplaceValue(255)

# Crear una lista de semillas
seeds = [
    [259, 272, 346],
    [264, 387, 233],
    [153, 260, 227],
    [357, 242, 234],
    [291, 233, 342]
]

# Agregar todas las semillas
for seed in seeds:
    connectedThreshold.AddSeed(seed)

RescaleType = itk.RescaleIntensityImageFilter[ImageType, ImageType]
rescaler = RescaleType.New()
rescaler.SetOutputMinimum(0)
rescaler.SetOutputMaximum(255)

# 5. Restar las imágenes
SubtractType = itk.SubtractImageFilter[ImageType, ImageType, ImageType]
subtractor = SubtractType.New()
subtractor2 = SubtractType.New()



#6. escritura
WriterType = itk.ImageFileWriter[OutputImageType]
writer = WriterType.New()
writer.SetFileName(OutputImage)


#Final. PipeLine


#original
subtractor.SetInput1(intensityFilter.GetOutput())
#cerebro
subtractor.SetInput2(medianFilter.GetOutput())
#Solo craneo
subtractor.Update()
intensityFilter.SetInput(subtractor.GetOutput())
#Los valores < 0 se ponen en 0 
intensityFilter.Update()

#guardar el craneo en una variable auxiliar
craneo = intensityFilter.GetOutput()

##restar hueso a original

intensityFilter2.SetInput(reader.GetOutput())
subtractor2.SetInput1(intensityFilter2.GetOutput())
subtractor2.SetInput2(intensityFilter.GetOutput())
subtractor2.Update()

# Ajustar los valores negativos a 0 en la imagen resultante
clampFilter = itk.ClampImageFilter[ImageType, ImageType].New()
clampFilter.SetInput(subtractor2.GetOutput())
clampFilter.SetBounds(0, 10000)  # Establece el límite inferior en 0
clampFilter.Update()

connectedThreshold.SetInput(clampFilter.GetOutput())
rescaler.SetInput(connectedThreshold.GetOutput())



writer.SetInput(rescaler.GetOutput())
writer.Update()