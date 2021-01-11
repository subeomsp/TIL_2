# Very Deep Convolutional Networks for Text Classification



## 1. 문제제기

​	기존의 CNN, LSTM을 활용한 NLP 모델의 경우 너무 '얕았다'

- 이미지 처리, 음성인식의 경우에는 CNN Layer를 깊게 쌓은 경우가 있었으나, NLP의 경우는 너무 얕았다.
- 이미지를 구조적으로 바라보았던 것처럼, 언어 또한 철자들이 모여 n-gram, 어간, 단어, 구문, 문장을 이루듯 구조적으로 바라보아야 한다.



## 2. 구조

 	1. 두가지 규칙에 의거
      	1. 레이어는 동일한 숫자의 피쳐 맵을 지닌다.
      	2. temporal resolution 이 반감할수록, 피쳐맵은 두배로 증가한다.

	### Convolution Layer Block

- 각 블록은 3개의 kernel size를 지닌 2개의 Convolutional Layer로 이루어져 있고, temporal BatchNormalization 을 사용하며, ReLU activation을 사용.
  - 이전 Yoon Kim의 CNN 논문에서의 Drop-out 대신 BatchNorm을 사용

