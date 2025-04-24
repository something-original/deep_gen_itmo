from styles import styles, styles_count, priors
import random

class StylesGenerator():
    def __init__(self, styles_, styles_count_, priors_):
        self.styles = styles_
        self.styles_count = styles_count_
        self.priors = priors_
        self.probabilities = {}
        self.generate_probs()

    def generate_probs(self):
        for category, items in self.styles.items():
            counts = self.styles_count[category]
            total = sum(counts)
            prior = self.priors[category]
            self.probabilities[category] = {
                item: (counts[idx] / total) * prior[item]
                for idx, item in enumerate(items)
            }

            total_prob = sum(self.probabilities[category].values())
            self.probabilities[category] = {
                item: prob / total_prob
                for item, prob in self.probabilities[category].items()
            }

    def generate_style(self, file_name):
        style = {}
        style_prob = 1

        for category in self.styles.keys():
            elems = self.styles[category]
            weights = (*self.probabilities[category].values(), )
            selected_item = random.choices(elems, weights=weights, k=1)[0]
            style_prob *= weights[elems.index(selected_item)]
            style[category] = selected_item

        style_string = '\n'.join([f'{cat}: {value}' for cat, value in style.items()])

        with open(file_name, 'w', encoding='utf-8-sig') as style_file:
            style_file.write(style_string + '\n')
            style_file.write(f'Вероятность: {style_prob:.4f}')


if __name__ == '__main__':
    styles_generator = StylesGenerator(styles, styles_count, priors)
    n_styles = 5
    for style_no in range(1, n_styles + 1):
        styles_generator.generate_style(f'style_{style_no}.txt')
