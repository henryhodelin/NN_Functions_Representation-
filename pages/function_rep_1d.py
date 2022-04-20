import numpy as np
import numexpr as ne
import tensorflow as tf
from streamlit_multipage import MultiPage
import plotly.graph_objects as go


def rep_1D_function_page(st, **state):
    st.header("1D Functions")

    st.header("Function Declaration")

    pi = np.pi

    col1, col2 = st.columns([1,2])
    with col1:
        
        st.header("Domain")
        values = st.slider( 'Select a range of values',
        0.0, 5.0, (0.0, 1.0))
        N_points = st.slider('Number of discretization points ', 0, 500, 200)
        #x_train  = np.linspace(values[0],values[1],N_points,endpoint=True)#Generate 100 points in the [0,2] interval
        #x_t      = np.zeros((len(x_train),1))
        #x_t[:,0] = x_train
        x  = np.linspace(values[0],values[1],N_points,endpoint=True)#Generate 100 points in the [0,2] interval
        x_t      = np.zeros((len(x),1))
        x_t[:,0] = x
        
        funcion = st.text_input('Function Declaration     f(x)=', 'sin(2*pi*x)')
        y = ne.evaluate(funcion)
        if st.button('View operators supported'):
                st.write("""
        Logical operators: &, |, ~

        -------------------------------------------------------
        Comparison operators: <, <=, ==, !=, >=, >

        -------------------------------------------------------
        Unary arithmetic operators: -

        -------------------------------------------------------
        Binary arithmetic operators: +, -, *, /, **, %, <<, >>
                """ )
        if st.button('View operators functions'):        
            st.write("""
        The next are the current supported set:    

        where(bool, number1, number2): number – number1 if the bool condition is true, number2 otherwise.
        
        
        -------------------------------------------------------

        {sin,cos,tan}(float|complex): float|complex – trigonometric sine, cosine or tangent.
        
        --------------------------------------------------------
        {arcsin,arccos,arctan}(float|complex): float|complex – trigonometric inverse sine, cosine or tangent.
        
        --------------------------------------------------------
        arctan2(float1, float2): float – trigonometric inverse tangent of float1/float2.
        
        ---------------------------------------------------------
        {sinh,cosh,tanh}(float|complex): float|complex – hyperbolic sine, cosine or tangent.

        ---------------------------------------------------------
        {arcsinh,arccosh,arctanh}(float|complex): float|complex – hyperbolic inverse sine, cosine or tangent.
        
        -----------------------------------------------------------
        {log,log10,log1p}(float|complex): float|complex – natural, base-10 and log(1+x) logarithms.
        
        -----------------------------------------------------------
        {exp,expm1}(float|complex): float|complex – exponential and exponential minus one.
        
        -----------------------------------------------------------
        sqrt(float|complex): float|complex – square root.

        -----------------------------------------------------------
        abs(float|complex): float|complex – absolute value.

        -----------------------------------------------------------
        conj(complex): complex – conjugate value.
        
        -----------------------------------------------------------
        {real,imag}(complex): float – real or imaginary part of complex.

        ------------------------------------------------------------
        complex(float, float): complex – complex from real and imaginary parts.

        ------------------------------------------------------------
        contains(str, str): bool – returns True for every string in op1 that contains op2.


            """ )
        st.button('Clear')    
    with col2:
        st.header('Function Graph')
        fig = go.Figure(data=go.Scatter(x=x, y=y,name='f(x)'))
        st.plotly_chart(fig, use_container_width=True)

        


    st.header("Neural Network Specifications")
    st.write("(SINGLE LAYER FEEDFORWARD NEURAL NETWORK)")

    class MyDenseLayer(tf.keras.layers.Layer):
        def __init__(self, num_outputs):
            super(MyDenseLayer, self).__init__()
            self.num_outputs = num_outputs
            
        def build(self, input_shape):
            self.kernel = self.add_weight("kernel",
            shape=[int(input_shape[-1]),self.num_outputs])
    
            self.biases = self.add_weight("kernel",shape=[ self.num_outputs])
        
        def call(self, input):
            #return tf.math.sigmoid(tf.math.add(tf.matmul(input, self.kernel),self.biases) )
            return tf.nn.relu(tf.math.add(tf.matmul(input, self.kernel),self.biases) )

    
    
    

    
    col1, col2 = st.columns([1,2])
    with col1:
        N_Neurons  = st.slider('Number of neurons', 0, 200, 25)
    
    inputs = tf.keras.Input(name='inputs',shape=(1),dtype=tf.dtypes.float32)
    hidden = MyDenseLayer(N_Neurons)
    output = tf.keras.layers.Dense(1,activation=None,name='output')
    model  = tf.keras.Sequential([inputs, hidden, output ])  


    st.header("Initial Neural Network Output")

    x_tf = tf.constant(x_t,dtype=float)
    z_tf =  model(x_tf)
    z = np.squeeze(z_tf.numpy())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y,
                    line = dict(color='royalblue', width=4, dash='dash'),
                    name='function'))
    fig.add_trace(go.Scatter(x=x, y=z,
                    mode='lines',
                    name='NN output'))


    #fig = go.Figure(data=go.Scatter(x=x, y=y,name='f(x)'))
    st.plotly_chart(fig, use_container_width=True)

    st.header("Training Parameters")
    st.write("(ADAM OPTIMIZER)")

    Col1, Col2 = st.columns([1,1])
    with Col1:
        epochs_units  = st.slider('Epoch units', 0, 9, 1,key = '1')
        epochs_power  = st.slider('Epoch power', 0, 9, 2,key = '2')
        epochs = epochs_units*10**epochs_power
        st.write('Epoch selected = '+str(epochs)) 

    with Col2:
        learning_rate_units = st.slider('Learning rate units', 0, 9, 1,key = '3')
        learning_rate_power = st.slider('Learning rate power', -9, -1, -3,key = '3')
        learning_rate_selected = learning_rate_units*10**learning_rate_power
        st.write('Learning rate = '+str(learning_rate_selected))

    Adam   = tf.keras.optimizers.Adam(learning_rate=learning_rate_selected, beta_1=0.9, beta_2=0.999, epsilon=1e-07)    

    x_tf = tf.constant(x_t,dtype=float)
    y_tf = tf.constant(y,dtype=float)
    trainable_vars = model.trainable_variables

    st.header('Training execution')

    losses =[]

    
    if st.checkbox('Execute Training'):
        my_bar = st.progress(0)
        for ix in range(epochs):
            with tf.GradientTape(persistent=True) as tape:
                tape.watch(x_tf)
                tape.watch(trainable_vars)
                f_x =  model(x_tf,training=True)
                t_loss = (y_tf -f_x)**2
                loss  =  tf.reduce_mean(t_loss)
                if ix == 0:
                    st.write('Initial loss = '+str(loss.numpy())  )
                    min_loss = loss.numpy()
                else:
                    if loss.numpy() < min_loss:
                        min_loss = loss.numpy()
                if ix == epochs-1:
                    st.write('Final loss = '+str(loss.numpy())  )
                tape.watch(loss)

            gradients = tape.gradient(loss, trainable_vars)
            Adam.apply_gradients(zip(gradients, trainable_vars))
            losses.append(loss.numpy())
            my_bar.progress(round(((ix+1)/epochs)*100))
        st.success('TRAINING ENDED! '+' Min Loss = '+str(min_loss))

        y_tf =  model(x_tf)
        y_NN = np.squeeze(y_tf.numpy())

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y,
                    line = dict(color='royalblue', width=4, dash='dash'),
                    name='function'))
        fig.add_trace(go.Scatter(x=x, y=y_NN,
                    mode='lines',
                    name='NN output'))


        #fig = go.Figure(data=go.Scatter(x=x, y=y,name='f(x)'))
        st.plotly_chart(fig, use_container_width=True)

    
    