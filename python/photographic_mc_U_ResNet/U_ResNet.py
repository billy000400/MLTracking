## A U-Net architecture for semantic image segmentation.
#
# No dense block is applied. Multiple inputs using "concatenate" instead of "add."
# Padding startegey is "same" instead of "valid."
# Using Conv2d transpose instead of upsampling2D

from tensorflow import keras
from tensorflow.keras import Model, initializers
from tensorflow.keras.layers import *

## A U-Net architecture for semantic image segmentation.
#
# No dense block is applied. Multiple inputs using "concatenate" instead of "add."
class U_ResNet:
    def __init__(self, input_shape, num_class, shrink_times=3):
        if len(input_shape) == 2:
            try:
                self.input_shape = input_shape + (1,)
            except:
                self.input_shape = input_shape + [1]
        elif len(input_shape) == 3:
            self.input_shape = input_shape
        else:
            perr("Invalid Input Shape")

        self.num_class = num_class
        self.shrink_times = shrink_times

    def get_model(self):

        init = initializers.RandomNormal(stddev=0.01)
        input = Input(self.input_shape)

        conv1 = Conv2D(64, 7, strides=1, padding='same', kernel_initializer=init)(input)
        conv1 = BatchNormalization()(conv1)
        conv1 = Activation("relu")(conv1)
        conv1 = Conv2D(64, 3, strides=1, padding='same', kernel_initializer=init)(conv1)
        conv1 = BatchNormalization()(conv1)
        conv1 = Activation("relu")(conv1)

        residual1 = Conv2D(128, 1, 2, padding='same', kernel_initializer=init)(conv1)
        pool1 = MaxPooling2D(pool_size=(2,2))(conv1)

        conv2 = Conv2D(128, 3, strides=1, padding="same", kernel_initializer=init)(pool1)
        conv2 = BatchNormalization()(conv2)
        conv2 = Activation("relu")(conv2)
        conv2 = Conv2D(128, 3, strides=1, padding="same", kernel_initializer=init)(conv2)
        conv2 = BatchNormalization()(conv2)
        conv2 = Activation("relu")(conv2)

        short_merge1 = Add()([residual1,conv2])
        residual2 = Conv2D(256, 1, 2, padding='same', kernel_initializer=init)(conv2)
        pool2 = MaxPooling2D(pool_size=(2,2))(short_merge1)

        conv3 = Conv2D(256, 3, strides=1, padding="same", kernel_initializer=init)(pool2)
        conv3 = BatchNormalization()(conv3)
        conv3 = Activation("relu")(conv3)
        conv3 = Conv2D(256, 3, strides=1, padding="same", kernel_initializer=init)(conv3)
        conv3 = BatchNormalization()(conv3)
        conv3 = Activation("relu")(conv3)

        short_merge2 = Add()([residual2, conv3])
        residual3 = Conv2D(512, 1, 2, padding='same', kernel_initializer=init)(conv3)
        pool3 = MaxPooling2D(pool_size=(2,2))(short_merge2)

        conv4 = Conv2D(512, 3, padding="same", kernel_initializer=init)(pool3)
        conv4 = BatchNormalization()(conv4)
        conv4 = Activation("relu")(conv4)
        conv4 = Conv2D(512, 3, padding="same", kernel_initializer=init)(conv4)
        conv4 = BatchNormalization()(conv4)
        conv4 = Activation("relu")(conv4)

        short_merge3 = Add()([residual3, conv4])
        pool4 = MaxPooling2D(pool_size=(2,2))(short_merge3)

        conv5 = Conv2D(1024, 3, padding="same", kernel_initializer=init)(pool4)
        conv5 = BatchNormalization()(conv5)
        conv5 = Activation("relu")(conv5)
        conv5 = Conv2D(1024, 3, padding="same", kernel_initializer=init)(conv5)
        conv5 = BatchNormalization()(conv5)
        conv5 = Activation("relu")(conv5)

        upconv1 = Conv2DTranspose(512, kernel_size=(2,2), strides=(2,2), padding='valid', kernel_initializer=init)(conv5)
        upconv1 = BatchNormalization()(upconv1)
        upconv1 = Activation('relu')(upconv1)
        merge1 = concatenate([upconv1, conv4], axis=3)

        conv6 = Conv2D(512, 3, padding='same', kernel_initializer=init)(merge1)
        conv6 = BatchNormalization()(conv6)
        conv6 = Activation('relu')(conv6)
        conv6 = Conv2D(512, 3, padding='same', kernel_initializer=init)(conv6)
        conv6 = BatchNormalization()(conv6)
        conv6 = Activation('relu')(conv6)

        upconv2 = Conv2DTranspose(256, kernel_size=(2,2), strides=(2,2), padding='valid', kernel_initializer=init)(conv6)
        upconv2 = BatchNormalization()(upconv2)
        upconv2 = Activation('relu')(upconv2)
        merge2 = concatenate([upconv2, conv3], axis=3)

        conv7 = Conv2D(256, 3, padding='same', kernel_initializer=init)(merge2)
        conv7 = BatchNormalization()(conv7)
        conv7 = Activation('relu')(conv7)
        conv7 = Conv2D(256, 3, padding='same', kernel_initializer=init)(conv7)
        conv7 = BatchNormalization()(conv7)
        conv7 = Activation('relu')(conv7)

        upconv3 = Conv2DTranspose(128, kernel_size=(2,2), strides=(2,2), padding='valid', kernel_initializer=init)(conv7)
        upconv3 = BatchNormalization()(upconv3)
        upconv3 = Activation('relu')(upconv3)
        merge3 = concatenate([upconv3, conv2],axis=3)

        conv8 = Conv2D(128, 3, padding='same', kernel_initializer=init)(merge3)
        conv8 = BatchNormalization()(conv8)
        conv8 = Activation('relu')(conv8)
        conv8 = Conv2D(128, 3, padding='same', kernel_initializer=init)(conv8)
        conv8 = BatchNormalization()(conv8)
        conv8 = Activation('relu')(conv8)

        upconv4 = Conv2DTranspose(64, kernel_size=(2,2), strides=(2,2), padding='valid', kernel_initializer=init)(conv8)
        upconv4 = BatchNormalization()(upconv4)
        upconv4 = Activation('relu')(upconv4)
        merge4 = concatenate([upconv4, conv1],axis=3)

        conv9 = Conv2D(64, 3, padding='same', kernel_initializer=init)(merge4)
        conv9 = BatchNormalization()(conv9)
        conv9 = Activation('relu')(conv9)
        conv9 = Conv2D(64, 3, padding='same', kernel_initializer=init)(conv9)
        conv9 = BatchNormalization()(conv9)
        conv9 = Activation('relu')(conv9)

        output = Conv2D(self.num_class, 1, activation='softmax', padding='same', kernel_initializer=init)(conv9)

        model = Model(input, output)
        return model

class U_small:
    def __init__(self, input_shape, num_class, shrink_times=3):
        if len(input_shape) == 2:
            try:
                self.input_shape = input_shape + (1,)
            except:
                self.input_shape = input_shape + [1]
        elif len(input_shape) == 3:
            self.input_shape = input_shape
        else:
            perr("Invalid Input Shape")

        self.num_class = num_class
        self.shrink_times = shrink_times

    def get_model(self):

        init = initializers.RandomNormal(stddev=0.01)
        input = Input(self.input_shape)

        conv1 = Conv2D(16, 3, strides=1, padding='same', kernel_initializer=init)(input)
        conv1 = BatchNormalization()(conv1)
        conv1 = Activation("relu")(conv1)
        conv1 = Conv2D(16, 3, strides=1, padding='same', kernel_initializer=init)(conv1)
        conv1 = BatchNormalization()(conv1)
        conv1 = Activation("relu")(conv1)

        pool1 = MaxPooling2D(pool_size=(2,2))(conv1)

        conv2 = Conv2D(32, 3, strides=1, padding="same", kernel_initializer=init)(pool1)
        conv2 = BatchNormalization()(conv2)
        conv2 = Activation("relu")(conv2)
        conv2 = Conv2D(32, 3, strides=1, padding="same", kernel_initializer=init)(conv2)
        conv2 = BatchNormalization()(conv2)
        conv2 = Activation("relu")(conv2)

        upconv1 = Conv2DTranspose(16, kernel_size=3, strides=2, padding='same', kernel_initializer=init)(conv2)
        upconv1 = BatchNormalization()(upconv1)
        upconv1 = Activation('relu')(upconv1)
        merge1 = concatenate([upconv1, conv1], axis=3)

        conv3 = Conv2D(16, 3, padding='same', kernel_initializer=init)(merge1)
        conv3 = BatchNormalization()(conv3)
        conv3 = Activation('relu')(conv3)
        conv3 = Conv2D(16, 3, padding='same', kernel_initializer=init)(conv3)
        conv3 = BatchNormalization()(conv3)
        conv3 = Activation('relu')(conv3)

        output = Conv2D(self.num_class, 1, activation='softmax', padding='same', kernel_initializer=init)(conv3)

        model = Model(input, output)
        return model

class U_ResNet_00:
    def __init__(self, input_shape, num_class, shrink_times=3):
        if len(input_shape) == 2:
            try:
                self.input_shape = input_shape + (1,)
            except:
                self.input_shape = input_shape + [1]
        elif len(input_shape) == 3:
            self.input_shape = input_shape
        else:
            perr("Invalid Input Shape")

        self.num_class = num_class
        self.shrink_times = shrink_times

    def get_model(self):

        init = initializers.RandomNormal(stddev=0.01)
        input = Input(self.input_shape)

        conv1 = Conv2D(64, 7, strides=1, padding='same', kernel_initializer=init)(input)
        conv1 = BatchNormalization()(conv1)
        conv1 = Activation("relu")(conv1)
        conv1 = Conv2D(64, 3, strides=1, padding='same', kernel_initializer=init)(conv1)
        conv1 = BatchNormalization()(conv1)
        conv1 = Activation("relu")(conv1)

        residual1 = Conv2D(128, 1, 2, padding='same', kernel_initializer=init)(conv1)
        pool1 = MaxPooling2D(pool_size=(2,2))(conv1)

        conv2 = Conv2D(128, 3, strides=1, padding="same", kernel_initializer=init)(pool1)
        conv2 = BatchNormalization()(conv2)
        conv2 = Activation("relu")(conv2)
        conv2 = Conv2D(128, 3, strides=1, padding="same", kernel_initializer=init)(conv2)
        conv2 = BatchNormalization()(conv2)
        conv2 = Activation("relu")(conv2)

        short_merge1 = Add()([residual1,conv2])
        residual2 = Conv2D(256, 1, 2, padding='same', kernel_initializer=init)(conv2)
        pool2 = MaxPooling2D(pool_size=(2,2))(short_merge1)

        conv3 = Conv2D(256, 3, strides=1, padding="same", kernel_initializer=init)(pool2)
        conv3 = BatchNormalization()(conv3)
        conv3 = Activation("relu")(conv3)
        conv3 = Conv2D(256, 3, strides=1, padding="same", kernel_initializer=init)(conv3)
        conv3 = BatchNormalization()(conv3)
        conv3 = Activation("relu")(conv3)

        short_merge2 = Add()([residual2, conv3])
        residual3 = Conv2D(512, 1, 2, padding='same', kernel_initializer=init)(conv3)
        pool3 = MaxPooling2D(pool_size=(2,2))(short_merge2)

        conv4 = Conv2D(512, 3, padding="same", kernel_initializer=init)(pool3)
        conv4 = BatchNormalization()(conv4)
        conv4 = Activation("relu")(conv4)
        conv4 = Conv2D(512, 3, padding="same", kernel_initializer=init)(conv4)
        conv4 = BatchNormalization()(conv4)
        conv4 = Activation("relu")(conv4)

        short_merge3 = Add()([residual3, conv4])
        pool4 = MaxPooling2D(pool_size=(2,2))(short_merge3)

        conv5 = Conv2D(1024, 3, padding="same", kernel_initializer=init)(pool4)
        conv5 = BatchNormalization()(conv5)
        conv5 = Activation("relu")(conv5)
        conv5 = Conv2D(1024, 3, padding="same", kernel_initializer=init)(conv5)
        conv5 = BatchNormalization()(conv5)
        conv5 = Activation("relu")(conv5)

        upconv1 = Conv2DTranspose(512, kernel_size=3, strides=2, padding='same', kernel_initializer=init)(conv5)
        upconv1 = BatchNormalization()(upconv1)
        upconv1 = Activation('relu')(upconv1)
        merge1 = concatenate([upconv1, conv4], axis=3)

        conv6 = Conv2D(512, 3, padding='same', kernel_initializer=init)(merge1)
        conv6 = BatchNormalization()(conv6)
        conv6 = Activation('relu')(conv6)
        conv6 = Conv2D(512, 3, padding='same', kernel_initializer=init)(conv6)
        conv6 = BatchNormalization()(conv6)
        conv6 = Activation('relu')(conv6)

        upconv2 = Conv2DTranspose(256, kernel_size=3, strides=2, padding='same', kernel_initializer=init)(conv6)
        upconv2 = BatchNormalization()(upconv2)
        upconv2 = Activation('relu')(upconv2)
        merge2 = concatenate([upconv2, conv3], axis=3)

        conv7 = Conv2D(256, 3, padding='same', kernel_initializer=init)(merge2)
        conv7 = BatchNormalization()(conv7)
        conv7 = Activation('relu')(conv7)
        conv7 = Conv2D(256, 3, padding='same', kernel_initializer=init)(conv7)
        conv7 = BatchNormalization()(conv7)
        conv7 = Activation('relu')(conv7)

        upconv3 = Conv2DTranspose(128, kernel_size=3, strides=2, padding='same', kernel_initializer=init)(conv7)
        upconv3 = BatchNormalization()(upconv3)
        upconv3 = Activation('relu')(upconv3)
        merge3 = concatenate([upconv3, conv2],axis=3)

        conv8 = Conv2D(128, 3, padding='same', kernel_initializer=init)(merge3)
        conv8 = BatchNormalization()(conv8)
        conv8 = Activation('relu')(conv8)
        conv8 = Conv2D(128, 3, padding='same', kernel_initializer=init)(conv8)
        conv8 = BatchNormalization()(conv8)
        conv8 = Activation('relu')(conv8)

        upconv4 = Conv2DTranspose(64, kernel_size=3, strides=2, padding='same', kernel_initializer=init)(conv8)
        upconv4 = BatchNormalization()(upconv4)
        upconv4 = Activation('relu')(upconv4)
        merge4 = concatenate([upconv4, conv1],axis=3)

        conv9 = Conv2D(64, 3, padding='same', kernel_initializer=init)(merge4)
        conv9 = BatchNormalization()(conv9)
        conv9 = Activation('relu')(conv9)
        conv9 = Conv2D(64, 3, padding='same', kernel_initializer=init)(conv9)
        conv9 = BatchNormalization()(conv9)
        conv9 = Activation('relu')(conv9)

        output = Conv2D(self.num_class, 1, activation='softmax', padding='same', kernel_initializer=init)(conv9)

        model = Model(input, output)
        return model

class U_ResNet_full:
    def __init__(self, input_shape, num_class, shrink_times=3):
        if len(input_shape) == 2:
            try:
                self.input_shape = input_shape + (1,)
            except:
                self.input_shape = input_shape + [1]
        elif len(input_shape) == 3:
            self.input_shape = input_shape
        else:
            perr("Invalid Input Shape")

        self.num_class = num_class
        self.shrink_times = shrink_times

    def get_model(self):

        init = initializers.RandomNormal(stddev=0.01)
        input = Input(self.input_shape)

        conv1 = Conv2D(64, 7, strides=1, padding='same', kernel_initializer=init)(input)
        conv1 = BatchNormalization()(conv1)
        conv1 = Activation("relu")(conv1)
        conv1 = Conv2D(64, 3, strides=1, padding='same', kernel_initializer=init)(conv1)
        conv1 = BatchNormalization()(conv1)
        conv1 = Activation("relu")(conv1)

        residual1 = Conv2D(128, 1, 2, padding='same', kernel_initializer=init)(conv1)
        pool1 = MaxPooling2D(pool_size=(2,2))(conv1)

        conv2 = Conv2D(128, 3, strides=1, padding="same", kernel_initializer=init)(pool1)
        conv2 = BatchNormalization()(conv2)
        conv2 = Activation("relu")(conv2)
        conv2 = Conv2D(128, 3, strides=1, padding="same", kernel_initializer=init)(conv2)
        conv2 = BatchNormalization()(conv2)
        conv2 = Activation("relu")(conv2)

        short_merge1 = Add()([residual1,conv2])
        residual2 = Conv2D(256, 1, 2, padding='same', kernel_initializer=init)(conv2)
        pool2 = MaxPooling2D(pool_size=(2,2))(short_merge1)

        conv3 = Conv2D(256, 3, strides=1, padding="same", kernel_initializer=init)(pool2)
        conv3 = BatchNormalization()(conv3)
        conv3 = Activation("relu")(conv3)
        conv3 = Conv2D(256, 3, strides=1, padding="same", kernel_initializer=init)(conv3)
        conv3 = BatchNormalization()(conv3)
        conv3 = Activation("relu")(conv3)

        short_merge2 = Add()([residual2, conv3])
        residual3 = Conv2D(512, 1, 2, padding='same', kernel_initializer=init)(conv3)
        pool3 = MaxPooling2D(pool_size=(2,2))(short_merge2)

        conv4 = Conv2D(512, 3, padding="same", kernel_initializer=init)(pool3)
        conv4 = BatchNormalization()(conv4)
        conv4 = Activation("relu")(conv4)
        conv4 = Conv2D(512, 3, padding="same", kernel_initializer=init)(conv4)
        conv4 = BatchNormalization()(conv4)
        conv4 = Activation("relu")(conv4)

        short_merge3 = Add()([residual3, conv4])
        pool4 = MaxPooling2D(pool_size=(2,2))(short_merge3)

        conv5 = Conv2D(1024, 3, padding="same", kernel_initializer=init)(pool4)
        conv5 = BatchNormalization()(conv5)
        conv5 = Activation("relu")(conv5)
        conv5 = Conv2D(1024, 3, padding="same", kernel_initializer=init)(conv5)
        conv5 = BatchNormalization()(conv5)
        conv5 = Activation("relu")(conv5)

        upconv1 = Conv2DTranspose(512, kernel_size=(2,2), strides=(2,2), padding='valid', kernel_initializer=init)(conv5)
        upconv1 = BatchNormalization()(upconv1)
        upconv1 = Activation('relu')(upconv1)
        merge1 = concatenate([upconv1, conv4], axis=3)

        conv6 = Conv2D(512, 3, padding='same', kernel_initializer=init)(merge1)
        conv6 = BatchNormalization()(conv6)
        conv6 = Activation('relu')(conv6)
        conv6 = Conv2D(512, 3, padding='same', kernel_initializer=init)(conv6)
        conv6 = BatchNormalization()(conv6)
        conv6 = Activation('relu')(conv6)

        upconv2 = Conv2DTranspose(256, kernel_size=(2,2), strides=(2,2), padding='valid', kernel_initializer=init)(conv6)
        upconv2 = BatchNormalization()(upconv2)
        upconv2 = Activation('relu')(upconv2)
        merge2 = concatenate([upconv2, conv3], axis=3)

        conv7 = Conv2D(256, 3, padding='same', kernel_initializer=init)(merge2)
        conv7 = BatchNormalization()(conv7)
        conv7 = Activation('relu')(conv7)
        conv7 = Conv2D(256, 3, padding='same', kernel_initializer=init)(conv7)
        conv7 = BatchNormalization()(conv7)
        conv7 = Activation('relu')(conv7)

        upconv3 = Conv2DTranspose(128, kernel_size=(2,2), strides=(2,2), padding='valid', kernel_initializer=init)(conv7)
        upconv3 = BatchNormalization()(upconv3)
        upconv3 = Activation('relu')(upconv3)
        merge3 = concatenate([upconv3, conv2],axis=3)

        conv8 = Conv2D(128, 3, padding='same', kernel_initializer=init)(merge3)
        conv8 = BatchNormalization()(conv8)
        conv8 = Activation('relu')(conv8)
        conv8 = Conv2D(128, 3, padding='same', kernel_initializer=init)(conv8)
        conv8 = BatchNormalization()(conv8)
        conv8 = Activation('relu')(conv8)

        upconv4 = Conv2DTranspose(64, kernel_size=(2,2), strides=(2,2), padding='valid', kernel_initializer=init)(conv8)
        upconv4 = BatchNormalization()(upconv4)
        upconv4 = Activation('relu')(upconv4)
        merge4 = concatenate([upconv4, conv1],axis=3)

        conv9 = Conv2D(64, 3, padding='same', kernel_initializer=init)(merge4)
        conv9 = BatchNormalization()(conv9)
        conv9 = Activation('relu')(conv9)
        conv9 = Conv2D(64, 3, padding='same', kernel_initializer=init)(conv9)
        conv9 = BatchNormalization()(conv9)
        conv9 = Activation('relu')(conv9)

        output = Conv2D(self.num_class, 1, activation='softmax', padding='same', kernel_initializer=init)(conv9)

        model = Model(input, output)
        return model
