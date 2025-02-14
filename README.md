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
  <!-- - Implicit ratings -->
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
    <!-- - behavior `<optional>` -->
    - rating
  - Evaluation:
    - RS: collaborative filtering and content-based information
    - CARS: pre-filtering, post-Filtering and contextual modeling paradigms

## Demo

AUTO-DataGenCARS+ has a user-freindly [demo](https://auto-datagencarsplus.ita.es/web/) based on Streamlit.
To use it, credentials are required and must be requested by sending an email to [mcrodriguez@ita.es](mcrodriguez@ita.es)
<!-- To use it the following credentials will be required. -->

<!-- - **user**: `autodatagencars`
- **password**: `Qxwsx3py` -->

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

Open source license: If you are creating an open source application under a license compatible with the GNU GPL license v3 you may use AUTO-DataGenCARS+ under its terms and conditions.

## Reference

Please make sure to cite the [paper](https://www.sciencedirect.com/science/article/pii/S157411921630270X) if you use
AUTO-DataGenCARS+ for your research:

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
@inproceedings{dexa2024,
	  author = {Marcos Caballero and María del Carmen Rodríguez-Hernández and Raúl Parada and Sergio Ilarri and Raquel Trillo-Lado and Ramón Hermoso and Óscar J. Rubio},
	  booktitle = {35th International Conference on Database and Expert Systems Applications (DEXA 2024), Naples (Italy)},
	  month = {August},
	  pages = {267--273},
	  publisher = {Springer, ISSN 0302-9743, ISSN 1611-3349 (electronic), Print ISBN 978-3-031-68308-4, Online ISBN 978-3-031-68309-1},
	  series = {Lecture Notes in Computer Science (LNCS)},
	  volume = {14910},
	  title = {An Approach for Social-Distance Preserving Location-Aware Recommender Systems: A Use Case in a Hospital Environment},
	  doi = {10.1007/978-3-031-68309-1_23},
	  year = {2024}
}
```

```
@inproceedings{momm2024,
	  author = {María del Carmen Rodríguez Hernández and Sergio Ilarri and Marcos Caballero and Raquel Trillo-Lado and Ramón Hermoso and Rafael del Hoyo Alonso},
	  booktitle = {22nd International Conference on Advances in Mobile Computing and Multimedia Intelligence (MoMM 2024), Bratislava (Slovakia)},
	  month = {December},
	  pages = {176--191},
	  title = {AUTO-DataGenCARS+: An Advanced User-Oriented Tool to Generate Data for the Evaluation of Recommender Systems},
	  year = {2024},
	  doi = {10.1007/978-3-031-78049-3_16},
	  series = {Lecture Notes in Computer Science (LNCS)},
	  publisher = {Springer, ISSN 0302-9743, ISSN 1611-3349 (electronic), Print ISBN 978-3-031-78048-6, Online ISBN 978-3-031-78049-3},
	  editor = {Pari Delir Haghighi and Solomiia Fedushko and Gabriele Kotsis and Ismail Khalil}
}
```

## Contributors

The following persons have contributed to AUTO-DataGenCARS+:

- María del Carmen Rodríguez Hernández - [mcrodriguez@ita.es](mcrodriguez@itainnova.es)
- Sergio Ilarri - [silarri@unizar.es](silarri@unizar.es)
- Raquel Trillo Lado - [raqueltl@unizar.es](raqueltl@unizar.es)
- Ramón Hermoso - [rhermoso@unizar.es](rhermoso@unizar.es)
- Marcos Caballero Yus - [mcaballero@ita.es](mcaballero@ita.es)
- Beatriz Franco García - [bfranco@ita.es](bfranco@ita.es)

## Acknowledgments

- Project PID2020-113037RB-I00 (funded by MICIU/AEI/10.13039/501100011033) — Next-gEnerATion dAta Management to foster suitable Behaviors and the resilience of cItizens against modErN ChallEnges (NEAT-AMBIENCE).
- Government of Aragon (COSMOS research group; last group reference: T64_23R; previous group reference: T64_20R).
- This work has also been partially funded by the Department of Big Data and Cognitive Systems at the Technological Institute of Aragon, by DGA-FSE IODIDE research group of the Government of Aragon (grant number T17_23R) and by the European Regional Development Fund (ERDF).
