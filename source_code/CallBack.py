import torch

class EarlyStopping():
    def __init__(self, patience = 5, verbose = False):
        self.patience = patience
        self.verbose = verbose      #Print log
        self.counter = 0            #Count useless epoch
        self.best_score = None      #Find best score
        self.early_stop = False

    def __call__(self, val):
        if self.best_score == None:
            self.best_score = val

        elif self.best_score >= val:
            #Increase counter
            self.counter += 1
            if self.verbose:
                print("Early stopping : {}/{}".format(self.counter, self.patience))

            #Check the counter, if it exceeds limit -> stop
            if self.counter == self.patience:
                self.early_stop = True

        else:
            #If best score < value, update the best score
            self.best_score = val
            self.counter = 0


class ModelCheckPoint():
    def __init__(self, path, verbose = False):
        self.best_acc = -1
        self.path = path            #print path
        self.verbose = verbose      #Print log
    def __call__(self, epoch, acc, model, optimize):
        if acc > self.best_acc:
            self.best_acc = acc
            #Save checkpoint
            checkpoint = {
                "epoch": epoch,
                "best_acc": self.best_acc,
                "model": model.state_dict(),
                "optimize": optimize.state_dict()
            }

            torch.save(checkpoint, self.path)
            if self.verbose:
                print("accuracy :{:.4f}".format(acc))
