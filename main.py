from utils.preprocessor import Preprocessor

if __name__ == "__main__":
    pre = Preprocessor(max_length= None, 
                    cased= False,
                    indreg = "datasets/indreg/",
                    semantic= "datasets/semantic/",
                    syntax= "datasets/syntax/"
                    )

    pre.preprocessor()