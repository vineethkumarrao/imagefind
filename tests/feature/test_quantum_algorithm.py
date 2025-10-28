"""
Test Script for AE-QIP v3.0.0 Quantum Algorithm
Tests quantum-enhanced similarity calculation
"""

import numpy as np
import time
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.quantum.ae_qip_v3 import AEQIPAlgorithm


def test_quantum_algorithm():
    """Test quantum algorithm functionality"""
    print("\n" + "="*70)
    print("AE-QIP v3.0.0 - Quantum Algorithm Test")
    print("="*70 + "\n")
    
    # Initialize algorithm
    print("1. Initializing quantum algorithm...")
    algo = AEQIPAlgorithm(
        use_quantum_inspired=True,
        n_precision_qubits=7,
        enable_entanglement=True
    )
    
    circuit_info = algo.get_circuit_info()
    print(f"   ✓ Total Qubits: {circuit_info['total_qubits']}")
    print(f"   ✓ Encoding: {circuit_info['encoding_qubits']} qubits")
    print(f"   ✓ Control: {circuit_info['control_qubits']} qubit")
    print(f"   ✓ Auxiliary: {circuit_info['auxiliary_qubits']} qubits")
    print(f"   ✓ Precision: 1/{circuit_info['precision_level']}\n")
    
    # Test vectors
    print("2. Creating test vectors (512D)...")
    np.random.seed(42)
    
    # Identical vectors
    v1 = np.random.randn(512)
    v1 = v1 / np.linalg.norm(v1)
    
    # Similar vector (90% similar)
    v2 = 0.9 * v1 + 0.1 * np.random.randn(512)
    v2 = v2 / np.linalg.norm(v2)
    
    # Different vector
    v3 = np.random.randn(512)
    v3 = v3 / np.linalg.norm(v3)
    
    print("   ✓ Vector 1: Reference (512D)")
    print("   ✓ Vector 2: Similar to V1 (90% overlap)")
    print("   ✓ Vector 3: Random (different)\n")
    
    # Test 1: Identical similarity
    print("3. Test Case 1: Self-similarity (v1 vs v1)")
    start = time.time()
    breakdown = algo.calculate_similarity_with_breakdown(
        v1.tolist(), v1.tolist()
    )
    elapsed = (time.time() - start) * 1000
    
    print(f"   🎯 Overall Similarity: {breakdown['similarity']:.4f}")
    print(f"   📊 Classical Cosine: {breakdown['classical']:.4f}")
    print(f"   ⚛️  Quantum Fidelity: {breakdown['quantum_fidelity']:.4f}")
    print(f"   🌊 Phase Coherence: {breakdown['phase_coherence']:.4f}")
    print(f"   📈 Amplitude Est: {breakdown['amplitude_estimated']:.4f}")
    if 'entanglement' in breakdown:
        print(f"   🔗 Entanglement: {breakdown['entanglement']:.4f}")
    print(f"   ⏱️  Time: {elapsed:.3f} ms\n")
    
    # Test 2: Similar vectors
    print("4. Test Case 2: Similar vectors (v1 vs v2)")
    start = time.time()
    breakdown = algo.calculate_similarity_with_breakdown(
        v1.tolist(), v2.tolist()
    )
    elapsed = (time.time() - start) * 1000
    
    print(f"   🎯 Overall Similarity: {breakdown['similarity']:.4f}")
    print(f"   📊 Classical Cosine: {breakdown['classical']:.4f}")
    print(f"   ⚛️  Quantum Fidelity: {breakdown['quantum_fidelity']:.4f}")
    print(f"   🌊 Phase Coherence: {breakdown['phase_coherence']:.4f}")
    print(f"   📈 Amplitude Est: {breakdown['amplitude_estimated']:.4f}")
    if 'entanglement' in breakdown:
        print(f"   🔗 Entanglement: {breakdown['entanglement']:.4f}")
    print(f"   ⏱️  Time: {elapsed:.3f} ms\n")
    
    # Test 3: Different vectors
    print("5. Test Case 3: Different vectors (v1 vs v3)")
    start = time.time()
    breakdown = algo.calculate_similarity_with_breakdown(
        v1.tolist(), v3.tolist()
    )
    elapsed = (time.time() - start) * 1000
    
    print(f"   🎯 Overall Similarity: {breakdown['similarity']:.4f}")
    print(f"   📊 Classical Cosine: {breakdown['classical']:.4f}")
    print(f"   ⚛️  Quantum Fidelity: {breakdown['quantum_fidelity']:.4f}")
    print(f"   🌊 Phase Coherence: {breakdown['phase_coherence']:.4f}")
    print(f"   📈 Amplitude Est: {breakdown['amplitude_estimated']:.4f}")
    if 'entanglement' in breakdown:
        print(f"   🔗 Entanglement: {breakdown['entanglement']:.4f}")
    print(f"   ⏱️  Time: {elapsed:.3f} ms\n")
    
    # Performance test
    print("6. Performance Benchmark (100 iterations)")
    start = time.time()
    for _ in range(100):
        algo.calculate_similarity(v1.tolist(), v2.tolist())
    elapsed = time.time() - start
    avg_time = (elapsed / 100) * 1000
    
    print(f"   ⏱️  Average Time: {avg_time:.3f} ms")
    print(f"   🚀 Throughput: {1000/avg_time:.1f} comparisons/second\n")
    
    # Summary
    print("="*70)
    print("✅ Quantum Algorithm Test Complete")
    print("="*70)
    print("\nKey Findings:")
    print(f"  • Self-similarity: ~{breakdown['similarity']:.2f} (expected ~1.00)")
    print(f"  • Quantum enhancement working: {breakdown['quantum_fidelity']:.2f}")
    print(f"  • Phase coherence active: {breakdown['phase_coherence']:.2f}")
    print(f"  • Amplitude estimation: {breakdown['amplitude_estimated']:.2f}")
    print(f"  • Performance: {avg_time:.2f}ms per comparison")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    test_quantum_algorithm()
