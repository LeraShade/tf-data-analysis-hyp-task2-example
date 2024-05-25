import pandas as pd
import numpy as np


chat_id = 5105487223 # Ваш chat ID, не меняйте название переменной

def solution(x: np.array, y: np.array) -> bool:
    # Создание DataFrame из массивов x и y
    data = pd.DataFrame({'group': x, 'revenue': y})
    
    # Добавление столбца 'converted' на основе значений 'revenue'
    data['converted'] = (data['revenue'] > 0).astype(int)
    
    # Разделение данных на группы контроля и теста
    control_group = data[data['group'] == 'control']
    test_group = data[data['group'] == 'test']

    # Проверка однородности групп по конверсии
    contingency_table = pd.crosstab(data['group'], data['converted'])
    chi2 = ((contingency_table - contingency_table.mean()) ** 2 / contingency_table.mean()).sum().sum()
    p_value = 1 - chi2.cdf(chi2, (contingency_table.shape[0] - 1) * (contingency_table.shape[1] - 1))

    if p_value < 0.02:
        print("Группы неоднородны по конверсии. Результаты теста могут быть недостоверными.")
        return False
    else:
        print("Группы однородны по конверсии. Продолжаем анализ.")

        # Расчет дохода на пользователя для каждой группы
        control_revenue_per_user = control_group['revenue'].mean()
        test_revenue_per_user = test_group['revenue'].mean()

        # Проверка статистической значимости различий в доходе на пользователя
        control_mean = control_group['revenue'].mean()
        control_std = control_group['revenue'].std()
        test_mean = test_group['revenue'].mean()
        test_std = test_group['revenue'].std()
        
        t_value = (test_mean - control_mean) / np.sqrt(control_std**2 / len(control_group) + test_std**2 / len(test_group))
        df = (control_std**2 / len(control_group) + test_std**2 / len(test_group))**2 / (control_std**4 / (len(control_group)**2 * (len(control_group) - 1)) + test_std**4 / (len(test_group)**2 * (len(test_group) - 1)))
        p_value = 2 * (1 - t.cdf(abs(t_value), df))

        if p_value < 0.05:
            print("Различия в доходе на пользователя статистически значимы.")
            
            # Расчет относительного изменения дохода на пользователя
            relative_change = (test_revenue_per_user - control_revenue_per_user) / control_revenue_per_user

            if relative_change > 0.08:
                print("Тест успешен. Повышение тарифа привело к увеличению дохода на пользователя более чем на 8%.")
                return True
            else:
                print("Тест не успешен. Повышение тарифа не привело к желаемому увеличению дохода на пользователя.")
                return False
        else:
            print("Различия в доходе на пользователя статистически не значимы. Тест не успешен.")
            return False
