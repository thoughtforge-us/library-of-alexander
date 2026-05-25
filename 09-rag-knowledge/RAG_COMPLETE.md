# 📚 RAG & Knowledge Systems — Complete Catalog

> Every RAG framework, vector database, and knowledge management tool.

---

## 🏆 Top RAG Projects

| Project | Stars | Description | Language |
|---------|-------|-------------|----------|
| [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | 81K | Leading open-source RAG engine | Python |
| [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) | 36K | Simple and fast RAG | Python |
| [microsoft/graphrag](https://github.com/microsoft/graphrag) | 33K | Graph-based RAG | Python |
| [NirDiamant/RAG_Techniques](https://github.com/NirDiamant/RAG_Techniques) | 28K | Advanced RAG techniques | Jupyter |
| [SciPhi-AI/R2R](https://github.com/SciPhi-AI/R2R) | 7.9K | Production-ready retrieval | Python |
| [weaviate/Verba](https://github.com/weaviate/Verba) | 7.7K | Weaviate RAG chatbot | Python |
| [Marker-Inc-Korea/AutoRAG](https://github.com/Marker-Inc-Korea/AutoRAG) | 4.8K | Auto-optimize RAG | Python |
| [truefoundry/cognita](https://github.com/truefoundry/cognita) | 4.4K | Modular RAG | Python |
| [run-llama/llama_index](https://github.com/run-llama/llama_index) | 50K | Document agent + RAG | Python |
| [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 138K | LLM framework + RAG | Python |

---

## 🗄️ Vector Databases

| Database | Stars | Type | License | Best For |
|----------|-------|------|---------|----------|
| [milvus-io/milvus](https://github.com/milvus-io/milvus) | 35K | Distributed | Apache 2.0 | Production scale |
| [qdrant/qdrant](https://github.com/qdrant/qdrant) | 23K | Rust-based | Apache 2.0 | Performance |
| [weaviate/weaviate](https://github.com/weaviate/weaviate) | 13K | Hybrid search | BSD-3 | Hybrid search |
| [chroma-core/chroma](https://github.com/chroma-core/chroma) | 19K | Embedded | Apache 2.0 | Development |
| [pgvector/pgvector](https://github.com/pgvector/pgvector) | 14K | PostgreSQL ext | PostgreSQL | Existing PG users |
| [lancedb/lancedb](https://github.com/lancedb/lancedb) | 6.5K | Embedded | Apache 2.0 | Serverless |
| [marqo-ai/marqo](https://github.com/marqo-ai/marqo) | 4.8K | Tensor search | Apache 2.0 | E-commerce |
| [vespa-engine/vespa](https://github.com/vespa-engine/vespa) | 6.2K | Big data | Apache 2.0 | Large scale |
| [pinecone-io/pinecone](https://github.com/pinecone-io/pinecone) | - | Managed | Proprietary | Serverless |
| [redis/redis](https://github.com/redis/redis) | 68K | In-memory | BSD-3 | Real-time |
| [opensearch-project/OpenSearch](https://github.com/opensearch-project/OpenSearch) | 10K | Search | Apache 2.0 | Full-text + vector |
| [Vald](https://github.com/vdaas/vald) | 1.7K | Distributed | Apache 2.0 | Cloud native |
| [tantivy-search/tantivy](https://github.com/tantivy-search/tantivy) | 12K | Rust search | MIT | Embedded |
| [facebooik/faiss](https://github.com/facebookresearch/faiss) | 32K | Similarity search | MIT | Research |
| [nmslib/hnswlib](https://github.com/nmslib/hnswlib) | 4.5K | HNSW | Apache 2.0 | Fast ANN |

---

## 🔍 RAG Techniques

### Basic Patterns
1. **Naive RAG** → Chunk → Embed → Retrieve → Generate
2. **Advanced RAG** → Query routing, reranking, hybrid search
3. **Modular RAG** → Flexible pipeline components
4. **Agentic RAG** → Agent decides when/how to retrieve

### Advanced Techniques (from RAG_Techniques repo)
- **Query Rewriting** — Improve retrieval with LLM-rewritten queries
- **HyDE** — Hypothetical Document Embeddings
- **Multi-Query** — Generate multiple queries for better coverage
- **Parent-Child Chunking** — Hierarchical document structure
- **Sentence Window** — Context around retrieved chunks
- **RAPTOR** — Recursive Abstractive Processing
- **Self-RAG** — Self-reflective retrieval
- **Corrective RAG (CRAG)** — Verify and correct retrieval
- **Graph RAG** — Knowledge graph + vector search
- **Adaptive RAG** — Dynamic retrieval strategy

---

## 📄 Document Processing

| Tool | Description | Stars |
|------|-------------|-------|
| [run-llama/llama_parse](https://github.com/run-llama/llama_parse) | Document parsing | - |
| [run-llama/liteparse](https://github.com/run-llama/liteparse) | Lightweight parsing | 59 |
| [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | OCR (78K stars) | 78K |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | NLP pipeline | - |
| [unstructured-io/unstructured](https://github.com/unstructured-io/unstructured) | Document processing | - |
| [Marker](https://github.com/datalab-to/marker) | PDF to Markdown | - |

---

## 🏗️ RAG Architecture Patterns

### Pattern 1: Basic RAG
```
Query → Embed → Vector Search → Top-K Chunks → Augment Prompt → LLM → Answer
```

### Pattern 2: Hybrid RAG
```
Query → [Vector Search + BM25] → Reranker → Top-K → Augment → LLM → Answer
```

### Pattern 3: Graph RAG
```
Query → Entity Extraction → Graph Traversal + Vector Search → Augment → LLM → Answer
```

### Pattern 4: Agentic RAG
```
Query → Agent → [Decide: Retrieve? Search? Calculate?] → Tools → LLM → Answer
```

### Pattern 5: Multi-Modal RAG
```
Query → [Text + Image + Table] → Multi-Modal Embedding → Search → Augment → LLM → Answer
```

---

*Last updated: 2026-05-25*


## 🆕 Auto-discovered nexus (2026-05-25 10:10 UTC)

| Repo | Stars | Lang | Description |
|------|-------|------|-------------|
| [facebook/rocksdb](https://github.com/facebook/rocksdb) | ⭐31697 | C++ | A library that provides an embeddable, persistent key-value store for  |
| [huggingface/sentence-transformers](https://github.com/huggingface/sentence-transformers) | ⭐18720 | Python | State-of-the-Art Embeddings, Retrieval, and Reranking |
| [Tencent/MMKV](https://github.com/Tencent/MMKV) | ⭐18593 | C++ | An efficient, small mobile key-value storage framework developed by We |
| [NVIDIA/nvidia-docker](https://github.com/NVIDIA/nvidia-docker) | ⭐17545 | None | Build and run Docker containers leveraging NVIDIA GPUs |
| [facebook/buck](https://github.com/facebook/buck) | ⭐8544 | Java | A fast build system that encourages the creation of small, reusable mo |
| [langchain-ai/rag-from-scratch](https://github.com/langchain-ai/rag-from-scratch) | ⭐8342 | Jupyter Notebook |  |
| [alibaba/AliSQL](https://github.com/alibaba/AliSQL) | ⭐5813 | C++ | AliSQL is a MySQL branch originated from Alibaba Group. Fetch document |
| [apple/embedding-atlas](https://github.com/apple/embedding-atlas) | ⭐4783 | TypeScript | Embedding Atlas is a tool that provides interactive visualizations for |
| [NVIDIA/nvidia-container-toolkit](https://github.com/NVIDIA/nvidia-container-toolkit) | ⭐4355 | Go | Build and run containers leveraging NVIDIA GPUs |
| [baidu/braft](https://github.com/baidu/braft) | ⭐4215 | C++ | An industrial-grade C++ implementation of RAFT consensus algorithm bas |
| [alibaba/Alink](https://github.com/alibaba/Alink) | ⭐3618 | Java | Alink is the Machine Learning algorithm platform based on Flink, devel |
| [Tencent/Tendis](https://github.com/Tencent/Tendis) | ⭐3142 | C++ | Tendis is a high-performance distributed storage system fully compatib |
| [NVIDIA/ChatRTX](https://github.com/NVIDIA/ChatRTX) | ⭐3123 | Python | A developer reference project for creating Retrieval Augmented Generat |
| [alibaba/euler](https://github.com/alibaba/euler) | ⭐2900 | C++ | A distributed graph deep learning framework. |
| [bytedance/scene](https://github.com/bytedance/scene) | ⭐2448 | Java | Android Single Activity Framework compatible with Fragment. |
| [alibaba/tair](https://github.com/alibaba/tair) | ⭐2306 | C++ | A distributed key-value storage system developed by Alibaba Group |
| [bytedance/terarkdb](https://github.com/bytedance/terarkdb) | ⭐2150 | C++ | A RocksDB compatible KV storage engine with better performance |
| [baidu/tera](https://github.com/baidu/tera) | ⭐1904 | C++ | An Internet-Scale Database. |
| [NVIDIA/aistore](https://github.com/NVIDIA/aistore) | ⭐1852 | Go | AIStore: scalable storage for AI applications |
| [THUDM/CogDL](https://github.com/THUDM/CogDL) | ⭐1821 | Python | CogDL: A Comprehensive Library for Graph Deep Learning (WWW 2023) |
| [PaddlePaddle/Research](https://github.com/PaddlePaddle/Research) | ⭐1758 | Python | novel deep learning research works with PaddlePaddle |
| [NVIDIA/dcgm-exporter](https://github.com/NVIDIA/dcgm-exporter) | ⭐1739 | Go | NVIDIA GPU metrics exporter for Prometheus leveraging DCGM |
| [Tencent/paxosstore](https://github.com/Tencent/paxosstore) | ⭐1715 | C++ | PaxosStore has been deployed in WeChat production for more than two ye |
| [intel/isa-l](https://github.com/intel/isa-l) | ⭐1079 | C | Intelligent Storage Acceleration Library |
| [OpenBMB/VisRAG](https://github.com/OpenBMB/VisRAG) | ⭐957 | Python | Parsing-free RAG supported by VLMs |
| [alibaba/EasyTransfer](https://github.com/alibaba/EasyTransfer) | ⭐862 | Python | EasyTransfer is designed to make the development of transfer learning  |
| [PaddlePaddle/RocketQA](https://github.com/PaddlePaddle/RocketQA) | ⭐785 | Python | 🚀 RocketQA, dense retrieval for information retrieval and question ans |
| [google-deepmind/reverb](https://github.com/google-deepmind/reverb) | ⭐779 | C++ | Reverb is an efficient and easy-to-use data storage and transport syst |
| [PaddlePaddle/Knover](https://github.com/PaddlePaddle/Knover) | ⭐671 | Python | Large-scale open domain KNOwledge grounded conVERsation system based o |
| [google-deepmind/limit](https://github.com/google-deepmind/limit) | ⭐650 | Jupyter Notebook | On the Theoretical Limitations of Embedding-Based Retrieval |
| [THUDM/GATNE](https://github.com/THUDM/GATNE) | ⭐536 | Python | Source code and dataset for KDD 2019 paper "Representation Learning fo |
| [alibaba/open-local](https://github.com/alibaba/open-local) | ⭐514 | Go | cloud-native local storage management system for stateful workload, lo |
| [huggingface/xet-core](https://github.com/huggingface/xet-core) | ⭐492 | Rust | xet client tech, used in huggingface_hub |
| [bytedance/vArmor](https://github.com/bytedance/vArmor) | ⭐475 | Go | vArmor is a cloud-native container hardening system that leverages App |
| [alibaba/schema-plugin-flow](https://github.com/alibaba/schema-plugin-flow) | ⭐424 | JavaScript | A highly extensible JavaScript library, abbreviated as Sifo. 一个高扩展性、可二 |
| [NVIDIA/workbench-example-hybrid-rag](https://github.com/NVIDIA/workbench-example-hybrid-rag) | ⭐368 | Python | An NVIDIA AI Workbench example project for Retrieval Augmented Generat |
| [TencentARC/VQFR](https://github.com/TencentARC/VQFR) | ⭐354 | Python | ECCV 2022, Oral, VQFR: Blind Face Restoration with Vector-Quantized Di |
| [NVIDIA/gds-nvidia-fs](https://github.com/NVIDIA/gds-nvidia-fs) | ⭐354 | C | NVIDIA GPUDirect Storage Driver |
| [langchain-ai/langconnect](https://github.com/langchain-ai/langconnect) | ⭐342 | Python | A managed RAG API server. |
| [bytedance/danmu.js](https://github.com/bytedance/danmu.js) | ⭐334 | JavaScript | HTML5 danmu (danmaku) plugin for any DOM element |
| [intel/tsffs](https://github.com/intel/tsffs) | ⭐329 | Rust | A snapshotting, coverage-guided fuzzer for software (UEFI, Kernel, fir |
| [Tencent/embedx](https://github.com/Tencent/embedx) | ⭐314 | C++ | embedx 是基于 c++ 开发的、完全自研的分布式 embedding 训练和推理框架。它目前支持 图模型、深度排序、召回模型和图与排序 |
| [google-deepmind/leo](https://github.com/google-deepmind/leo) | ⭐311 | Python | Implementation of Meta-Learning with Latent Embedding Optimization |
| [baidu/knowledge-driven-dialogue](https://github.com/baidu/knowledge-driven-dialogue) | ⭐269 | Python | baseline system of knowledge driven dialogue competition |
| [google-deepmind/grid-cells](https://github.com/google-deepmind/grid-cells) | ⭐263 | Python | Implementation of the supervised learning experiments in Vector-based  |
| [THUDM/KOBE](https://github.com/THUDM/KOBE) | ⭐243 | Python | Towards Knowledge-Based Personalized Product Description Generation in |
| [THUDM/NLP4Rec-Papers](https://github.com/THUDM/NLP4Rec-Papers) | ⭐230 | None | Paper list of NLP for recommender systems |
| [OpenBMB/RAGEval](https://github.com/OpenBMB/RAGEval) | ⭐230 | Python |  |
| [intel/ScalableVectorSearch](https://github.com/intel/ScalableVectorSearch) | ⭐224 | C++ |  |
| [alibaba/hangzhou_house_knowledge](https://github.com/alibaba/hangzhou_house_knowledge) | ⭐207 | CSS | 2017年买房经历总结出来的买房购房知识分享给大家，希望对大家有所帮助。买房不易，且买且珍惜。Sharing the knowledge o |


## 🆕 Auto-discovered nexus (2026-05-25 14:10 UTC)

| Repo | Stars | Lang | Description |
|------|-------|------|-------------|
| [bytedance/ParaGen](https://github.com/bytedance/ParaGen) | ⭐185 | Python | ParaGen is a PyTorch deep learning framework for parallel sequence gen |
| [openai/train-procgen](https://github.com/openai/train-procgen) | ⭐182 | Python | Code for the paper "Leveraging Procedural Generation to Benchmark Rein |
| [alibaba/nann](https://github.com/alibaba/nann) | ⭐171 | C++ | A flexible, high-performance framework for large-scale retrieval probl |
| [intel/pmem-csi](https://github.com/intel/pmem-csi) | ⭐164 | Go | Persistent Memory Container Storage Interface Driver |
| [intel/virtual-storage-manager](https://github.com/intel/virtual-storage-manager) | ⭐160 | Python |  |
| [openai/gym3](https://github.com/openai/gym3) | ⭐147 | Python | Vectorized interface for reinforcement learning environments |
| [OpenGVLab/Hulk](https://github.com/OpenGVLab/Hulk) | ⭐144 | Python | An official implementation of "Hulk: A Universal Knowledge Translator  |
| [THUDM/KBRD](https://github.com/THUDM/KBRD) | ⭐134 | Python | Towards Knowledge-Based Recommender Dialog System @ EMNLP 2019 |
| [intel/yask](https://github.com/intel/yask) | ⭐118 | C++ | YASK--Yet Another Stencil Kit: a domain-specific language and framewor |
| [bytedance/R2Former](https://github.com/bytedance/R2Former) | ⭐104 | Jupyter Notebook | Official repository for R2Former: Unified Retrieval and Reranking Tran |
| [intel/neuro-vectorizer](https://github.com/intel/neuro-vectorizer) | ⭐99 | C | NeuroVectorizer is a framework that uses deep reinforcement learning ( |
| [alibaba/neug](https://github.com/alibaba/neug) | ⭐97 | C++ | High-performance embedded graph database for analytics and real-time t |
| [NVIDIA/l2fwd-nv](https://github.com/NVIDIA/l2fwd-nv) | ⭐90 | C++ | l2fwd-nv provides an example of how to leverage your DPDK network appl |
| [PaddlePaddle/PaddleDTX](https://github.com/PaddlePaddle/PaddleDTX) | ⭐88 | Go | Paddle with Decentralized Trust based on Xuperchain |
| [OpenGVLab/Awesome-DragGAN](https://github.com/OpenGVLab/Awesome-DragGAN) | ⭐82 | None | Awesome-DragGAN: A curated list of papers, tutorials, repositories rel |
| [apple/ml-knowledge-conflicts](https://github.com/apple/ml-knowledge-conflicts) | ⭐78 | Python | Entity-Based Knowledge Conflicts in Question Answering. Code repo for  |
| [THUDM/SelfKG](https://github.com/THUDM/SelfKG) | ⭐75 | Python | Codes for WWW2022 accepted paper: SelfKG: Self-Supervised Entity Align |
| [THUDM/CogKR](https://github.com/THUDM/CogKR) | ⭐71 | Python | Source code and dataset for paper "Cognitive Knowledge Graph Reasoning |
| [NVIDIA/multi-storage-client](https://github.com/NVIDIA/multi-storage-client) | ⭐71 | Python | Unified high-performance Python client for object and file stores. |
| [openai/openai-knowledge-retrieval](https://github.com/openai/openai-knowledge-retrieval) | ⭐70 | Python | OS repo for Knowledge Retrieval starter kit |
| [bytedance/cryostar](https://github.com/bytedance/cryostar) | ⭐67 | Python | Leveraging Structural Priors and Constraints for Cryo-EM Heterogeneous |
| [huggingface/ai-blueprint](https://github.com/huggingface/ai-blueprint) | ⭐65 | Jupyter Notebook | A blueprint for AI development, focusing on applied examples of RAG, i |
| [google-deepmind/xtr](https://github.com/google-deepmind/xtr) | ⭐64 | Jupyter Notebook | XTR: Rethinking the Role of Token Retrieval in Multi-Vector Retrieval |
| [OpenBMB/ParamMute](https://github.com/OpenBMB/ParamMute) | ⭐60 | Python | ParamMute: Suppressing Knowledge-Critical FFNs for Faithful Retrieval- |
| [apple/ml-fct](https://github.com/apple/ml-fct) | ⭐55 | Python | Research publication code for "Forward Compatible Training for Large-S |
| [langchain-ai/langchain-milvus](https://github.com/langchain-ai/langchain-milvus) | ⭐54 | Python | The LangChain wrapper of Milvus vector database for efficient vector s |
| [TencentARC/BEBR](https://github.com/TencentARC/BEBR) | ⭐45 | Python | Official code for "Binary embedding based retrieval at Tencent" |
| [NVIDIA/cuEmbed](https://github.com/NVIDIA/cuEmbed) | ⭐45 | Cuda | CUDA Embedding Lookup Kernel Library |
| [bytedance/BytevalKit-Emb](https://github.com/bytedance/BytevalKit-Emb) | ⭐42 | Python | BytevalKit-Emb is a modular embedding model evaluation framework that  |
| [OpenBMB/MoRE](https://github.com/OpenBMB/MoRE) | ⭐41 | Python | [SIGIR '26] Mixture-of-Retrieval Experts for Reasoning-Guided Multimod |
| [Tencent/vectordatabase-sdk-python](https://github.com/Tencent/vectordatabase-sdk-python) | ⭐40 | Python | Tencent VectorDB Python SDK |
| [alibaba/vector-accelerating-unit](https://github.com/alibaba/vector-accelerating-unit) | ⭐36 | C++ | vector accelerating unit |
| [intel/accelerator-solution-zoo](https://github.com/intel/accelerator-solution-zoo) | ⭐31 | C | Intel accelerators Zoo, like one of its solution Intel® Vector Data St |
| [apple/ml-acn-embed](https://github.com/apple/ml-acn-embed) | ⭐29 | Python | Acoustic Neighbor Embeddings |
| [OpenBMB/DEBATER](https://github.com/OpenBMB/DEBATER) | ⭐28 | Python | This is the code repo for our paper "Learning More Effective Represent |
| [OpenBMB/UltraLink](https://github.com/OpenBMB/UltraLink) | ⭐28 | Python | An Open-Source Knowledge-Enhanced Multilingual Supervised Fine-tuning  |
| [OpenBMB/RAG-DDR](https://github.com/OpenBMB/RAG-DDR) | ⭐24 | Python | This is the code repo for the paper "RAG-DDR: Optimizing Retrieval-Aug |
| [apple/ml-kge](https://github.com/apple/ml-kge) | ⭐24 | Python | Multilingual Knowledge Graph Enhancement (EMNLP 2023) |
| [NVIDIA/5t5g](https://github.com/NVIDIA/5t5g) | ⭐23 | C++ | This project shows how to leverage your DPDK network application with  |
| [Tencent/vectordatabase-sdk-java](https://github.com/Tencent/vectordatabase-sdk-java) | ⭐22 | Java | Tencent VectorDB Java SDK |
| [intel/Enterprise-RAG](https://github.com/intel/Enterprise-RAG) | ⭐20 | Python | Intel® AI for Enterprise RAG converts enterprise data into actionable  |
| [huggingface/ember](https://github.com/huggingface/ember) | ⭐19 | Python | ANE accelerated embedding models! |
| [Tencent/nf-tencentcloud](https://github.com/Tencent/nf-tencentcloud) | ⭐18 | Java | nf-tencentcloud is a nextflow plugin designed to add Tencent Cloud Obj |
| [NVIDIA/nvmesh-kernel](https://github.com/NVIDIA/nvmesh-kernel) | ⭐18 | C | NVMesh by NVIDIA provides remote shared storage facilities with in-ser |
| [NVIDIA/nv-embedding-cache](https://github.com/NVIDIA/nv-embedding-cache) | ⭐18 | C++ | Fast hierarchical embedding cache for recommenders |
| [facebook/bookworm](https://github.com/facebook/bookworm) | ⭐18 | Ruby | Bookworm is a program that gleans context from a Chef/Ruby codebase le |
| [Tencent/vectordatabase-sdk-go](https://github.com/Tencent/vectordatabase-sdk-go) | ⭐17 | Go | Tencent VectorDB Golang SDK |
| [alibaba/SimCSE-with-CARDS](https://github.com/alibaba/SimCSE-with-CARDS) | ⭐16 | Python | Source code for SIGIR 2022 paper.  |
| [intel/document-automation](https://github.com/intel/document-automation) | ⭐16 | Python | Document Automation Reference Kit |
| [alibaba/DiskVecLab](https://github.com/alibaba/DiskVecLab) | ⭐13 | C++ | A modular framework for evaluating disk-based vector search, enabling  |
