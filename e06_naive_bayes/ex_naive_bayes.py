"""
Implement a naive Bayes classificator for spam emails.

We supply a database of spam/ham emails as well as a small library to read it.
The database is in the subfolder database. All spam mails are in
database/spam_mails, all ham emails in database/ham_emails.

To load the database write

    db = spamAssassinDatabase.SpamAssassinDatabase(data_path='./database',
                                                   training_test_ratio=.75)

The data_path parameter gives the path to the database, the training_test_ratio
defines which part of the database should be read as training data and which
part should be used as test data.

You can then access the data with:

    word_count_spam = {}
    word_count_ham = {}

    for mail in db.read_training_mails():
        for w in mail.words:
             if mail.label == 'spam':
                 word_count_spam[w] += 1
             elif mail.label == 'ham':
                 word_count_ham[w] += 1

You can use the word frequency to estimate the probabilities p(x|c).
"""
import spamAssassinDatabase
import random


class NaiveBayes(object):
    def __init__(self, database):
        db = spamAssassinDatabase.SpamAssassinDatabase(data_path='./database', training_test_ratio=.75)
        word_count_spam = {}
        word_count_ham = {}
        self.prob_spam = {}
        self.prob_ham = {}
        self.prob_mail = 0.0
        self.mail_ham = 0.0
        spam_count = 0
        ham_count = 0
        for mail in db.read_training_mails():
            for w in mail.words:
                if mail.label == 'spam':
                    spam_count += 1
                    if w in word_count_spam:
                        word_count_spam[w] += 1
                    else:
                        word_count_spam[w] = 1
                elif mail.label == 'ham':
                    ham_count += 1
                    if w in word_count_ham:
                        word_count_ham[w] += 1
                    else:
                        word_count_ham[w] = 1
        
        for key in word_count_spam:
            if key in word_count_ham:
                ham = word_count_ham[key]
            else:
                ham = 0
            self.prob_spam[key] = float(word_count_spam[key]) / (word_count_spam[key] + ham)
        for key in word_count_ham:
            if key in word_count_spam:
                spam = word_count_spam[key]
            else:
                spam = 0
            self.prob_ham[key] = float(word_count_ham[key]) / (word_count_ham[key] + spam)
        
        self.prob_mail = float(spam_count) / (spam_count + ham_count)
        self.mail_ham = float(ham_count) / (ham_count + spam_count)
            
                 
                 
    def spam_prob(self, email):
        spam_p = self.prob_mail
        ham_p = self.mail_ham
        for w in email.words:
            if w in self.prob_spam:
                if self.prob_spam[w] > 0:
                    spam_p += self.prob_spam[w]
            if w in self.prob_ham:
                if self.prob_ham[w] > 0:
                    ham_p += self.prob_ham[w]
        
        
        if len(email.words) == 0:
            spam_p = 1
        else:
           # print spam_p, ham_p
            spam_p = spam_p / (spam_p + ham_p)            

        
        return spam_p


def main():
    db = spamAssassinDatabase.SpamAssassinDatabase(data_path='./database',
                                                   training_test_ratio=.75)

    nb = NaiveBayes(db)

    for n, mail in enumerate(db.read_test_mails()):
        prob = nb.spam_prob(mail)
        correct = ((prob > .5 and mail.label == 'spam')
                   or (prob <= .5 and mail.label == 'ham'))
        if correct is False:
            print("Mail {} -- p(c|x) = {} -- is {} -- Labeling correct: {}"
              .format(n, prob, mail.label, correct))


if __name__ == '__main__':
    main()
