import streamlit as st



def show_tutorial_page():

    st.title("""SUMOnet Python Package Tutorial""")
    st.markdown('<p style="font-size: 2rem;font-family:monospace">You can install SUMOnet as a python package as well</p>',unsafe_allow_html=True)
    st.code("""
    pip install sumonet
    """)

    st.markdown('<p style="font-size: 2rem;font-family:monospace">1) Loading Data </p>',unsafe_allow_html=True)
    st.markdown('<p style="font-family:monospace">You can use our experimental data by using <strong>Data Class</strong></p>',unsafe_allow_html=True)
    st.markdown('<ul><li>By using <strong>Data</strong> class - It does not take any input variable and returns our dbPTM data as Train and Test samples and their labels</li><li>Data class gives <code>X_train</code>, <code>X_test</code> as a list of strings (21-mers), so you need to encode them</li><li><code>y_train</code> and <code>y_test</code> are lists of integers (labels), so you need to convert them to a 2-d array for feeding our model.</li></ul>',unsafe_allow_html=True)

    st.code("""
    from sumonet.utils.data_pipe import Data
    data = Data()
    X_train, y_train, X_test, y_test = data.load_sumonet_experiment_data()
    """)

    st.markdown('<p>Example for Training sequences: <code>[RTSHLKQCAVKMEVGPQLLLQ, EDSARPGAHAKVKKLFVGGLK, EKEPPGQLQVKAQPQARMTVP, NMMKTSEAKIKHFDGEDYTCI, PVQKHAIPIIKEKRDLMACAQ]</code></p>',unsafe_allow_html=True)
    st.markdown('<p>Example for Training labels: <code>[1, 1, 1, 1, 1]</code></p>',unsafe_allow_html=True)

    st.markdown("***")

    st.markdown('<p style="font-size: 2rem;font-family:monospace">2) Encoding </p>',unsafe_allow_html=True)
    st.markdown('<p><strong>Encoding class</strong> takes 2 parameters: <code>encoderTypes</code> and <code>scaler</code>.</p>',unsafe_allow_html=True)
    st.markdown('<ul><li><code>encoderTypes</code> is initially defined as <code>blosum62</code> according to our experiments, but you can use <code>one-hot</code> or <code>nlf</code> also.</li><li><code>scaler</code> is initially defined as <strong>True</strong> according to our experiments. It means that data will be passed into min-max scaler. If you want, you can cancel it.</li><li>You can change the encoder type with the <code>set_encoder_type(encoderType)</code> function.</li></ul>',unsafe_allow_html=True)

    st.code("""
    from sumonet.utils.encodings import Encoding
    encoder = Encoding(encoderType='one-hot') ## Encoding(encoderType = 'blosum62', scale = True)
    X_train_encoded = encoder.encode_data(X_train)
    """)

    st.markdown("***")

    st.markdown('<p style="font-size: 2rem;font-family:monospace">3) SUMOnet Model </p>',unsafe_allow_html=True)
    st.markdown('<ul><li>You can use our architecture with randomly initialized weights.</li><li>You can also use our pre-trained model in two different weights: <ol><li>Model that was trained on the entire data (Train + Test) - This model is in production.</li><li>Model that was trained only on Training data - If you want to use our test data to avoid information leak.</li></ol></li></ul>',unsafe_allow_html=True)
    st.markdown("<p><strong>Important Note:</strong> <em>SUMOnet</em> will be initialized with the input shape of <em>blosum62</em> encoded vectors.</p>",unsafe_allow_html=True)
    st.markdown('<p>First we need to get 2d array for training</p>',unsafe_allow_html=True)
    st.code("""
    import numpy as np
    y_train = np.asarray(y_train)
    y_train = (y_train[:,None] == np.arange(2)).astype(int)
    """)
    st.markdown('<p>Now we can train randomly initialized SUMOnet model</p>',unsafe_allow_html=True)
    st.code("""
    from sumonet.model.architecture import SUMOnet
    model = SUMOnet(input_shape = X_train_encoded.shape[1:] ) #Input shape is the shape of blosum62 vector in default. But you can set your input shape for randomly initialized models.
    model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
    model.fit(X_train_encoded,y_train,epochs=3)
    """)
    st.markdown('<p style="font-size: 1rem;font-family:monospace">You can use pre-trained models</p>',unsafe_allow_html=True)
    st.markdown('<ul><li>You can also use our pre-trained model in two different weights: <ol><li>Model that was trained on the entire data (Train + Test) - This model is in production.</li><li>Model that was trained only on Training data - If you want to use our test data to avoid information leak.</li></ol></li></ul>',unsafe_allow_html=True)
    st.code("""
    from sumonet.model.architecture import SUMOnet
    SUMOnet3_model = SUMOnet()
    SUMOnet3_model.load_weights()
    #This model was trained on entire (Train + Test) data! If you want to use model that was trained on only Train samples please use load_weights(model_state='on_train_data')
    """)

    st.markdown('<p>Now we can make predictions</p>',unsafe_allow_html=True)
    st.code("""
    encoder = Encoding(encoderType='blosum62') ## Firstly we need to encode our test data
    X_test_encoded = encoder.encode_data(X_test)
    y_preds = SUMOnet3_model.predict(X_test_encoded)
    """)
    
    st.markdown("***")

    st.markdown('<p style="font-size: 2rem;font-family:monospace">4) Lets Evaluate  Results</p>',unsafe_allow_html=True)
    st.markdown('<p>Evaluate functions are organized according to our evaluation set-up so you can use them directly in comparisons</p>',unsafe_allow_html=True)
    st.markdown("<p><strong>evaluate</strong> function takes 3 arguments:</p>",unsafe_allow_html=True)
    st.markdown("<ul><li><code>y_test</code>: Gold labels should be in 1-d, so if yours is 2-d like ours, use <code>argmax(-1)</code>.</li><li><code>y_pred</code>: Predictions are already in a 2-d vector format.</li><li>String or array that includes metrics.</li></ul>",unsafe_allow_html=True)

    st.code("""
    y_test = np.asarray(y_test) #Convert list of integers to 2d array
    y_test = (y_test[:,None] == np.arange(2)).astype(int)
            
    f1_score = evaluate(y_test.argmax(-1),y_preds,'f1')
    mcc = evaluate(y_test.argmax(-1),y_preds,'mcc')
    roc = evaluate(y_test.argmax(-1),y_preds,'roc')
    aupr = evaluate(y_test.argmax(-1),y_preds,'aupr')
    """)

    st.markdown("<p>You can calculate all results at once.</p>",unsafe_allow_html=True)
    st.markdown("<p>This calculation outputs a dictionary.</p>",unsafe_allow_html=True)

    st.code("""
    evaluate(y_test.argmax(-1),y_preds,['f1','mcc','roc','aupr'])
    """)

    st.markdown("<pre>{'aupr': 0.7598319565641193, 'f1': 0.6580921757770631, 'mcc': 0.5694399870602478, 'roc': 0.8713018549625735}</pre>",unsafe_allow_html=True)