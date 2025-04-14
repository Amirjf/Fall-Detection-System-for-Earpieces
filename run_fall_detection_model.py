from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Conv1D, MaxPooling1D, Flatten, Dense, Dropout
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt



def plot_confusion(y_true, y_pred, labels=[0, 1], class_names=['ADL', 'Fall']):
    """
    Plots a confusion matrix using seaborn heatmap.

    Parameters:
    - y_true: Ground truth labels
    - y_pred: Predicted labels
    - labels: List of class indices (default: [0, 1])
    - class_names: List of class names for axis labels
    """
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.show()
    
def run_fall_detection_model(X_acc, X_all, y, 
                             use_gyro=False,
                             apply_smote=True,
                             epochs=20,
                             batch_size=32,
                             test_size=0.2,
                             verbose=True):
    """
    Trains and evaluates a CNN model for fall detection using accelerometer and gyroscope data.

    Parameters:
    - X_acc: ndarray of shape (n_samples, 300, 3)
    - X_all: ndarray of shape (n_samples, 300, 6)
    - y: ndarray of shape (n_samples,)
    - use_gyro: bool, whether to use accelerometer+gyroscope data (default=False)
    - apply_smote: bool, whether to apply SMOTE oversampling (default=True)
    - epochs: int, training epochs (default=20)
    - batch_size: int, batch size (default=32)
    - test_size: float, test set ratio (default=0.2)
    - verbose: bool, print logs (default=True)
    """
    
    # Select features
    X = X_all if use_gyro else X_acc
    X_2d = X.reshape((X.shape[0], -1))
    
    # Remove NaNs
    mask = ~np.isnan(X_2d).any(axis=1)
    X_clean = X_2d[mask]
    y_clean = y[mask]
    
    if verbose:
        print(f"Removed {len(y) - len(y_clean)} samples due to NaNs.")
    
    # Apply SMOTE
    if apply_smote:
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X_clean, y_clean)
        X_resampled = X_resampled.reshape((-1, 300, X.shape[2]))
        if verbose:
            print("✅ SMOTE applied")
            print("X shape:", X_resampled.shape)
            print("Label counts:", np.bincount(y_resampled))
    else:
        X_resampled = X_clean.reshape((-1, 300, X.shape[2]))
        y_resampled = y_clean
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=test_size, stratify=y_resampled, random_state=42)
    
    # CNN model
    model = Sequential([
        Input(shape=(300, X.shape[2])),
        Conv1D(filters=32, kernel_size=5, activation='relu'),
        MaxPooling1D(pool_size=2),
        Conv1D(filters=64, kernel_size=5, activation='relu'),
        MaxPooling1D(pool_size=2),
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
                        validation_split=0.2, verbose=verbose)
    
    # Evaluate
    loss, acc = model.evaluate(X_test, y_test, verbose=0)
    
    y_pred = (model.predict(X_test) > 0.5).astype("int32")

    plot_confusion(y_test, y_pred)

    print(f"\n✅ Test Accuracy: {acc:.2f}")


    
    print("\n📝 Classification Report:")
    print(classification_report(y_test, y_pred))

    return model, history