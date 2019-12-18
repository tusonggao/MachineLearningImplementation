# https://en.wikipedia.org/wiki/Slope_One

class SlopeOne(object):
    def __init__(self):
        self.diffs = {}
        self.freqs = {}

    def _compute_freqs_diffs(self, userdata):  # 计算统计信息
        freqs, diffs = {}, {}
        for ratings in userdata.values():
            for item1, rating1 in ratings.items():
                freqs.setdefault(item1, {})
                diffs.setdefault(item1, {})
                for item2, rating2 in ratings.items():
                    freqs[item1].setdefault(item2, 0)
                    diffs[item1].setdefault(item2, 0.0)
                    freqs[item1][item2] += 1
                    diffs[item1][item2] += rating1 - rating2
        for item1, ratings in diffs.items():
            for item2 in ratings:
                ratings[item2] /= freqs[item1][item2]
        return freqs, diffs

    def fit(self, userdata):  # 使用用户打分数据进行训练
        self.freqs, self.diffs = self._compute_freqs_diffs(userdata)

    def update(self, userdata):  # 使用新的用户打分数据，更新统计信息，适用于在线学习
        freqs_new, diffs_new = self._compute_freqs_diffs(userdata)

        for item1 in freqs_new:
            for item2 in freqs_new:
                if item1 == item2:
                    continue
                if item1 not in self.diffs:
                    self.freqs[item1], self.diffs[item1] = {}, {}
                if item2 in self.freqs[item1]:
                    diffs_sum = (freqs_new[item1][item2] * diffs_new[item1][item2] +
                                 self.freqs[item1][item2] * self.diffs[item1][item2])
                    self.freqs[item1][item2] += freqs_new[item1][item2]
                    self.diffs[item1][item2] = diffs_sum / self.freqs[item1][item2]
                else:
                    self.freqs[item1][item2] = freqs_new[item1][item2]
                    self.diffs[item1][item2] = diffs_new[item1][item2]

    def predict(self, userprefs):  # 预测
        preds, freqs = {}, {}
        for item, rating in userprefs.items():
            for diffitem, diffratings in self.diffs.items():
                try:
                    freq = self.freqs[diffitem][item]
                except KeyError:
                    continue
                preds.setdefault(diffitem, 0.0)
                freqs.setdefault(diffitem, 0)
                preds[diffitem] += freq * (diffratings[item] + rating)
                freqs[diffitem] += freq
        return dict([(item, value / freqs[item])
                     for item, value in preds.items()
                     if item not in userprefs and freqs[item] > 0])


# Python code to demonstrate working of unittest
import unittest

class TestSlopeOneAlgo(unittest.TestCase):
    def setUp(self):
        pass

    def test_fit_func(self):
        # case 1
        s = SlopeOne()
        userdata = dict(
            alice=dict(squid=1.0, cuttlefish=0.5, octopus=0.2),
            bob=dict(squid=1.0, octopus=0.5, nautilus=0.2),
            carole=dict(squid=0.2, octopus=1.0, cuttlefish=0.4, nautilus=0.4),
            dave=dict(cuttlefish=0.9, octopus=0.4, nautilus=0.5),
        )
        s.fit(userdata)
        outcome = s.predict(dict(squid=0.4))
        # {'cuttlefish': 0.25, 'octopus': 0.23333333333333336, 'nautilus': 0.09999999999999998}

        self.assertEqual(len(outcome), 3)
        self.assertAlmostEqual(outcome['cuttlefish'], 0.25)
        self.assertAlmostEqual(outcome['octopus'], 0.23333333333333336)
        self.assertAlmostEqual(outcome['nautilus'], 0.09999999999999998)

        # case 2
        s = SlopeOne()
        userdata = dict(
            alice=dict(squid=1.0, cuttlefish=0.5, octopus=0.2),
            bob=dict(squid=1.0, octopus=0.5, nautilus=0.2),
            carole=dict(squid=0.2, octopus=1.0, cuttlefish=0.4, nautilus=0.4),
            dave=dict(cuttlefish=0.9, octopus=0.4, nautilus=0.5),
        )
        s.fit(userdata)
        outcome = s.predict(dict(squid=0.4, nautilus=0.6))
        # {'cuttlefish': 0.525, 'octopus': 0.55}

        self.assertEqual(len(outcome), 2)
        self.assertAlmostEqual(outcome['cuttlefish'], 0.525)
        self.assertAlmostEqual(outcome['octopus'], 0.55)

    def test_update_func(self):
        s = SlopeOne()
        userdata = dict(
            alice=dict(squid=1.0, cuttlefish=0.5, octopus=0.2),
            bob=dict(squid=1.0, octopus=0.5, nautilus=0.2),
            carole=dict(squid=0.2, octopus=1.0, cuttlefish=0.4, nautilus=0.4),
        )
        s.fit(userdata)
        userdata1 = dict(
            dave=dict(cuttlefish=0.9, octopus=0.4, nautilus=0.5),
        )
        s.update(userdata1)
        outcome = s.predict(dict(squid=0.4))

        self.assertEqual(len(outcome), 3)
        self.assertAlmostEqual(outcome['cuttlefish'], 0.25)
        self.assertAlmostEqual(outcome['octopus'], 0.23333333333333336)
        self.assertAlmostEqual(outcome['nautilus'], 0.09999999999999998)

if __name__ == '__main__':
    unittest.main()

# if __name__ == '__main__':
#     s = SlopeOne()
#
#     userdata = dict(
#         alice=dict(squid=1.0, cuttlefish=0.5, octopus=0.2),
#         bob=dict(squid=1.0, octopus=0.5, nautilus=0.2),
#         carole=dict(squid=0.2, octopus=1.0, cuttlefish=0.4, nautilus=0.4),
#     )
#
#     s.fit(userdata)
#
#     userdata1 = dict(
#         dave=dict(cuttlefish=0.9, octopus=0.4, nautilus=0.5),
#     )
#
#     s.update(userdata1)
#
#     # userdata1 = dict(
#     #     dave={'cuttlefish': 0.25, 'squid': 0.78},
#     # )
#     #
#     # s.update(userdata1)
#
#     print(s.predict(dict(squid=0.4)))
#
#     # {'cuttlefish': 0.25, 'octopus': 0.23333333333333336, 'nautilus': 0.09999999999999998}
#
#     print(s.predict(dict(squid=0.4, nautilus=0.6)))
#
#     # {'cuttlefish': 0.525, 'octopus': 0.55}
#
#
#     # userdata = dict(
#     #     John=dict(A=5.0, B=3, C=2),
#     #     Mark=dict(A=3.0, B=4),
#     # )
#     #
#
#     # print(s.predict(dict(B=2, C=5)))



