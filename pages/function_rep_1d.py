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
        st.header("Function Graph")
        fig = go.Figure(data=go.Scatter(x=x, y=y,name='f(x)'))
        st.plotly_chart(fig, use_container_width=True)
