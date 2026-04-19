import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from pages.supabase import ler_tabela

res = ler_tabela('login')
print("Result:", res)
