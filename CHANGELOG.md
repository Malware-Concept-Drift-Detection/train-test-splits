## [1.2.1](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/compare/1.2.0...1.2.1) (2025-08-04)

### Bug Fixes

* families removal when filtering duplicates ([363c528](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/363c5285b62ca9e4a1cfebfb86b870d5836c8050))

## [1.2.0](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/compare/1.1.2...1.2.0) (2025-08-04)

### Features

* split using only non-duplicated samples ([c7c0589](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/c7c05892e520636033cead2fcbc476c99a83a8b1))

### General maintenance

* update script to run extraction of TheFinalDataset and Norton670 ([33ad579](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/33ad57908a0a30fb67d719a66fa94efb82326de6))

## [1.1.2](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/compare/1.1.1...1.1.2) (2025-07-29)

### Bug Fixes

* remove tesseract import ([847b3fe](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/847b3fe6cd664e53a18de2e2ef6a79e953ad3ede))

### General maintenance

* remove print in config ([0f0a21a](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/0f0a21a24b56f30055a1e802551304fc2d305068))
* update script ([e653a32](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/e653a32286836a30baecdcc244a702dc4ae59a43))

### Refactoring

* unique package for all splits ([1da26f4](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/1da26f40f4400733de534b50a37093ec2b6a90fc))

## [1.1.1](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/compare/1.1.0...1.1.1) (2025-06-03)

### Bug Fixes

* bisection method ([752528f](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/752528f81d9e3390ed9b1e72e836f1b8905403dc))

## [1.1.0](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/compare/1.0.1...1.1.0) (2025-05-28)

### Features

* best time split generalized for TheFinalDataset directory structure ([41332d7](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/41332d71540d920b9a644c7125f446ffb586d7bd))
* extend time-based split to TheFinalDataset directory format ([d3e5ec5](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/d3e5ec5736973e646e44766aae225c319aff4e4e))

### Dependency updates

* **deps:** add matplotlib ([03acff8](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/03acff83d21cd905625d54560436d7f57f9a9087))

### Refactoring

* move norton best time-based split to a common package ([aefd053](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/aefd053bcab632476453276162968303cd4d3c9e))

## [1.0.1](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/compare/1.0.0...1.0.1) (2025-05-18)

### Bug Fixes

* trunc family csv path ([a87ff32](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/a87ff3225f9e3ea22e2085a52823eda0026d3654))

### General maintenance

* format code, add ruff dep ([d99e952](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/d99e9523b0629be96e6235b1adcd9464c32afc79))

## 1.0.0 (2025-05-18)

### Features

* add random and time based train test split for ember ([5f77630](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/5f776301555747a702266a8ce4e940fb21e1485b))
* norton split with and without raw dataset ([b4cc630](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/b4cc63092d34aa0ad1dcf081aa46ff02f4242ce7))

### General maintenance

* add gitignore ([c95a86a](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/c95a86a546670ad58ee6851222d099e411e45708))
* add script to run the pipeline ([43d5716](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/43d5716612794b33bec238f2815f8948a774d499))
* add template files (poetry and ci) ([9722192](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/97221921aacabf7014362bc9dd9fa0aa4b8a90a2))
* refine dockerfile, rm requirements ([839f09d](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/839f09df8b174eb05741859e7196955614224607))
* restore requirements.txt ([2886084](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/2886084e7e495e774ab26a52980f83358ee135f2))
* rm docker compose and refine script + minor adjustments ([24d2081](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/24d2081bf5df390eeebdb05836cce20f123be988))

### Refactoring

* add split package ([4a2c3e8](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/4a2c3e85548b77e66a3d5a47e649e0a4dbe285ad))
* move code, writing motif splits ([78c7a9d](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/78c7a9d2596eec8fbe0ee7e7d3c3f2152f36516b))
* rename package ([d14951d](https://github.com/Malware-Concept-Drift-Detection/train-test-splits/commit/d14951d651e0fd678545cf08b2ebe2a87755ca36))
