# OptimizedOfficeAI

# 가상환경 생성
conda create --name OOA python=3.9.16

# 가상환경 활성화
conda activate OOA

# GPU사용을 위한 CUDA & cudnn 설치
conda install -c conda-forge cudatoolkit=11.8 cudnn=8.7.0

# tensorflow 프레임워크 설치
conda install "tensorflow<2.11"

# tensorflow GPU 테스트
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

# DJANGO 4.2.2 버전 설치
conda install -c conda-forge django=4.2.2

# matplotlib 4.2.2 버전 설치
conda install matplotlib=4.2.2

# nbformat 5.7.0 버전 설치
conda install nbformat=5.7.0

# 
