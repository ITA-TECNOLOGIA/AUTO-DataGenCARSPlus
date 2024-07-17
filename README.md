<div style="text-align:center"><img src="./resources/icons/logo-autodatagencarsplus.png" /></div>

## Overview

AUTO_DataGenCARS+ is a complete Python-based synthetic dataset generator for the valuation of Traditional Recommendation Systems (RS) and Context-Aware Recommendation Systems (CARS).

The generator presents features such as:

- A flexible definition of user profiles, use, item and context schemas.
- A realistic generation of ratings (implicit and explicit) and attributes of items.
- The possibility to mix real and synthetic datasets.
- Functionalities to analyze existing datasets as a basis for synthetic data generation.
- Support for the automatic mapping between item schemas and Java classes.
- Analysis and evaluation of RS anc CARS with generated datasets.

It was designed with the following purposes:

* Generate a synthetic dataset:
  - Explicit ratings
  - Implicit ratings
* Pre-process a dataset:
  - Generate NULL values
  - Replace NULL values
  - Generate user profile (manual and automatic)
  - Replicate dataset
  - Extend dataset
  - Recalculate ratings
  - Transform attributes
* Analysis of a dataset:
  - Visualization:
    - user
    - item
    - context `<optional>`
    - behavior `<optional>`
    - rating
  - Evaluation:
    - RS: collaborative filtering and content-based information
    - CARS: pre-filtering, post-Filtering and contextual modeling paradigms

## Demo

AUTO-DataGenCARS has a user-freindly [demo](https://auto-datagencarsplus.ita.es/web/) based on Streamlit.
To use it the following credentials will be required.

- **user**: `autodatagencars`
- **password**: `Qxwsx3py`

<!-- ## Installation:
With pip:
```python
    $ pip install numpy
    $ pip install scikit-surprise
```
With conda:
```python
    $ conda install -c conda-forge scikit-surprise
```

For the latest version, you can also clone the repo and build the source:
```python   
    $ git clone https://git.itainnova.es/bigdata/misc/auto_datagencars.git  
``` -->

## Requirements

The libraries used in this project with its respective versions can be seen in `environment.yml`.

## License

Open source license: If you are creating an open source application under a license compatible with the GNU GPL license v3 you may use AUTO-DataGenCARS under its terms and conditions.

## Reference

Please make sure to cite the [paper](https://www.sciencedirect.com/science/article/pii/S157411921630270X) if you use
AUTO-DataGenCARS for your research:

```
@article{mc2017datagencars,
         title = {DataGenCARS: A generator of synthetic data for the evaluation of context-aware recommendation systems},
         journal = {Pervasive and Mobile Computing},                      
         note = {Special Issue IEEE International Conference on Pervasive Computing and Communications (PerCom) 2016},
         year = {2017},
         publisher = {Elsevier},
         doi = {10.1016/j.pmcj.2016.09.020},      
         volume = {38},
         number = {2},
         pages = {516-541},
         issn = {1574-1192},
         author = {María del Carmen Rodríguez-Hernández and Sergio Ilarri and Ramón Hermoso and Raquel Trillo-Lado}         
        }
```

```
@inproceedings{mc2024autodatagencarsplus,   
        title = {An Approach for Social-Distance Preserving Location-Aware Recommender Systems: A Use Case in a Hospital Environment},        
        author = {Marcos Caballero and María del Carmen Rodríguez-Hernández and Raúl Parada and Sergio Ilarri and Raquel Trillo-Lado and Ramón Hermoso and Óscar Rubio}, 
        booktitle = {35th DEXA Conferences and Workshops},    
        year = {2024},        
        pages = {1-6},  
        publisher = {Springer}
        }
```

## Contributors

The following persons have contributed to AUTO-DataGenCARS:

- María del Carmen Rodríguez Hernández - [mcrodriguez@itainnova.es](mcrodriguez@itainnova.es)
- Sergio Ilarri - [silarri@unizar.es](silarri@unizar.es)
- Raquel Trillo Lado - [raqueltl@unizar.es](raqueltl@unizar.es)
- Ramón Hermoso - [rhermoso@unizar.es](rhermoso@unizar.es)
- Marcos Caballero Yus - [mcaballero@itainnova.es](mcaballero@itainnova.es)
- Beatriz Franco García - [bfranco@itainnova.es](bfranco@itainnova.es)
