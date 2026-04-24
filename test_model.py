import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from brain import StudyAssistant
import time

def run_advanced_evaluation():
    # 1. Initialize the Assistant
    print("Initializing Robust RAG Assistant...")
    assistant = StudyAssistant()
    refusal_message = "I cannot answer this from the provided chapter content."

    # 2. Load the evaluation set
    df = pd.read_csv('evaluation_set.csv')
    X_test = df['question'].tolist()
    
    # Ground Truth: 1 if answerable, 0 if it should be refused
    y_test = [0 if t in ['out_of_scope', 'adversarial'] else 1 for t in df['expected_type']]

    # 3. Execution Loop
    y_pred = []
    latencies = []
    
    print(f"Starting Evaluation on {len(X_test)} samples...")
    for i, question in enumerate(X_test):
        start_time = time.time()
        
        # Get response
        response_chunks = list(assistant.answer(question))
        response = "".join(response_chunks)
        
        latencies.append(time.time() - start_time)
        
        # Classification logic
        if refusal_message in response:
            y_pred.append(0)
        else:
            y_pred.append(1)
            
        print(f"[{i+1}/{len(X_test)}] Q: {question[:40]}... -> {'Refused' if y_pred[-1]==0 else 'Answered'}")

    # 4. Metrics Calculation
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    avg_lat = np.mean(latencies)
    
    # 5. Confusion Matrix Analysis
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    # 6. Report Generation
    print("\n" + "="*40)
    print("       RAG SYSTEM AUDIT REPORT")
    print("="*40)
    print(f"Accuracy:  {acc*100:.2f}%")
    print(f"Precision: {prec*100:.2f}% (How many answered were correct?)")
    print(f"Recall:    {rec*100:.2f}% (How many answerable were caught?)")
    print(f"F1-Score:  {f1*100:.2f}%")
    print(f"Avg Latency: {avg_lat:.2f}s")
    print("-" * 40)
    print(f"True Positives (Answered correctly):  {tp}")
    print(f"True Negatives (Refused correctly):   {tn}")
    print(f"False Positives (Hallucinations?):   {fp}")
    print(f"False Negatives (Wrongly refused):    {fn}")
    print("="*40)

    # 7. Failure Breakdown
    df['prediction'] = y_pred
    failures = df[df['prediction'] != y_test]
    if not failures.empty:
        print("\nDETAILED FAILURE ANALYSIS:")
        print(failures[['question', 'expected_type', 'prediction']])
    else:
        print("\nNo failures! System is robust.")

if __name__ == "__main__":
    run_advanced_evaluation()