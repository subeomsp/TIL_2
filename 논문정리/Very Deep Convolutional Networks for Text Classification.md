# Very Deep Convolutional Networks for Text Classification



## 1. 문제제기

​	기존의 CNN, LSTM을 활용한 NLP 모델의 경우 너무 '얕았다'

- 이미지 처리, 음성인식의 경우에는 CNN Layer를 깊게 쌓은 경우가 있었으나, NLP의 경우는 너무 얕았다.
- 이미지를 구조적으로 바라보았던 것처럼, 언어 또한 철자들이 모여 n-gram, 어간, 단어, 구문, 문장을 이루듯 구조적으로 바라보아야 한다.



## 2. 구조

- 레이어는 동일한 숫자의 피쳐 맵을 지닌다.

  temporal resolution 이 반감할수록, 피쳐맵은 두배로 증가한다.

- 기존 NLP 모델의 경우 6개까지의 layer만을 사용하고, 서로 다른 size의 convolution을 합쳤다.

  - 해당 논문의 경우 3이란 작은 convolution을 가진 Layer 4개를 쌓아 9개 토큰들의 span을 생성한다.

    이를 통해 network는 스스로 최적의 '3-gram feature'를 생성할 수 있다. 

	### Convolution Layer Block

- 각 블록은 3개의 kernel size를 지닌 2개의 Convolutional Layer로 이루어져 있고, temporal BatchNormalization 을 사용하며, ReLU activation을 사용.
  - **BatchNormalization**
    - 결국 목적은 gradient 소실, 혹은 폭발을 방지하기 위함
    - Training 시에는 mini-batch의 평균과 분산으로 normalize, Test시에는 계산해놓은 이동 평균으로 normalize
      - CNN의 경우 미니배치 사이즈 x feature map size(p x q) 마다의 평균과 분산을 구해 normalize 실행
  - 이전 Yoon Kim의 CNN 논문에서의 Drop-out 대신 BatchNorm을 사용



## 3. 학습

- 2015년 Zhang et al.과 똑같은 코퍼스를 사용하여 측정하였으나 현 논문의 모델이 더 좋은 성과를 나타냄
  - Layer가 깊어질 수록 유리하다
- 세부 사항
  - Word Level이 아닌 Character Level (69 token - 영어, 숫자, 기호)
  - 1014의 고정된 Input size with padding
  - Character Embedding은 16
  - SGD
  - mini-batch size 128
  - learning rate 0.01 / momentum 0.9
- 결과
  - 깊이가 깊어질수록 더 좋은 성능을 보인다.
    - 하지만 depth가 일정 수준 이상으로 높아지게 되면 성능이 떨어지는데 optimize 과정에서의 문제
      - 역전파 과정에서 gradient가 소실되고, SGD가 loss function을 잘 잡아내지 못함
  - Max-pooling이 다른 pooling보다 좋은 성능을 보인다



## 4. 결론

**BENEFIT OF DEPTH**

- 조그마한 사이즈의 layer를 여러개 쌓아라.

#### 이미지, 음성인식에서 연구되고 있는 것들을 NLP로 끌어들여와라...?



