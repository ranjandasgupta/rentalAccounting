const api = (path, options={}) => fetch(path, { headers: { 'Content-Type': 'application/json' }, ...options })
  .then(r => { if(!r.ok) throw new Error('Request failed'); return r.json(); })
  .catch(e => { alert(e.message); throw e; });

// Tabs
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(btn.dataset.tab).classList.add('active');
  });
});

// Helpers
function toTable(elId, data) {
  const el = document.getElementById(elId);
  if(!Array.isArray(data)) data = [data];
  if (data.length === 0) { el.innerHTML = '<tr><td>No data</td></tr>'; return; }
  const cols = Object.keys(data[0]);
  const thead = '<tr>' + cols.map(c => `<th>${c}</th>`).join('') + '</tr>';
  const rows = data.map(row => '<tr>' + cols.map(c => `<td>${row[c] ?? ''}</td>`).join('') + '</tr>').join('');
  el.innerHTML = thead + rows;
}

function loadTable(path, elId) {
  api(path).then(data => toTable(elId, data));
}

// Create functions
function createCompany() {
  const body = {
    name: document.getElementById('company-name').value,
    tin: document.getElementById('company-tin').value || null
  };
  api('/api/companies', { method: 'POST', body: JSON.stringify(body) }).then(() => alert('Company created'));
}

function createProperty() {
  const body = {
    company_id: parseInt(document.getElementById('property-company').value, 10),
    address: document.getElementById('property-address').value,
    description: document.getElementById('property-desc').value || null
  };
  api('/api/properties', { method: 'POST', body: JSON.stringify(body) }).then(() => alert('Property created'));
}

function createTenant() {
  const body = {
    name: document.getElementById('tenant-name').value,
    phone: document.getElementById('tenant-phone').value || null,
    email: document.getElementById('tenant-email').value || null,
  };
  api('/api/tenants', { method: 'POST', body: JSON.stringify(body) }).then(() => alert('Tenant created'));
}

function createLease() {
  const body = {
    tenant_id: parseInt(document.getElementById('lease-tenant').value, 10),
    property_id: parseInt(document.getElementById('lease-property').value, 10),
    from_date: document.getElementById('lease-from').value,
    to_date: document.getElementById('lease-to').value || null
  };
  api('/api/leases', { method: 'POST', body: JSON.stringify(body) }).then(() => alert('Lease created'));
}

function createRent() {
  const body = {
    property_id: parseInt(document.getElementById('rent-property').value, 10),
    from_date: document.getElementById('rent-from').value,
    to_date: document.getElementById('rent-to').value || null,
    amount: parseFloat(document.getElementById('rent-amount').value)
  };
  api('/api/rents', { method: 'POST', body: JSON.stringify(body) }).then(() => alert('Rent created'));
}

function createAccountType() {
  const body = {
    code: document.getElementById('atype-code').value.toUpperCase(),
    name: document.getElementById('atype-name').value,
    description: document.getElementById('atype-desc').value || null
  };
  api('/api/account-types', { method: 'POST', body: JSON.stringify(body) }).then(() => alert('Account type created'));
}

function createAccountSubType() {
  const body = {
    type_id: parseInt(document.getElementById('asub-typeid').value, 10),
    code: document.getElementById('asub-code').value,
    name: document.getElementById('asub-name').value,
    description: document.getElementById('asub-desc').value || null
  };
  api('/api/account-subtypes', { method: 'POST', body: JSON.stringify(body) }).then(() => alert('SubType created'));
}

function createAccount() {
  const sub = document.getElementById('acct-subtypeid').value;
  const body = {
    type_id: parseInt(document.getElementById('acct-typeid').value, 10),
    sub_type_id: sub ? parseInt(sub,10) : null,
    name: document.getElementById('acct-name').value,
    description: document.getElementById('acct-desc').value || null
  };
  api('/api/accounts', { method: 'POST', body: JSON.stringify(body) }).then(() => alert('Account created'));
}

function createTransaction() {
  const prop = document.getElementById('trans-prop').value;
  const ten = document.getElementById('trans-tenant').value;
  const body = {
    debit_account_id: parseInt(document.getElementById('trans-debit').value, 10),
    credit_account_id: parseInt(document.getElementById('trans-credit').value, 10),
    property_id: prop ? parseInt(prop,10) : null,
    tenant_id: ten ? parseInt(ten,10) : null,
    date: document.getElementById('trans-date').value,
    amount: parseFloat(document.getElementById('trans-amount').value),
    description: document.getElementById('trans-desc').value || null
  };
  api('/api/transactions', { method: 'POST', body: JSON.stringify(body) }).then(() => alert('Transaction posted'));
}

// Reports
function runIncomeStatement() {
  const s = document.getElementById('is-start').value;
  const e = document.getElementById('is-end').value;
  api(`/api/reports/income-statement?start_date=${s}&end_date=${e}`).then(d => {
    document.getElementById('is-output').textContent = JSON.stringify(d, null, 2);
  });
}
function runBalanceSheet() {
  const a = document.getElementById('bs-asof').value;
  api(`/api/reports/balance-sheet?as_of=${a}`).then(d => {
    document.getElementById('bs-output').textContent = JSON.stringify(d, null, 2);
  });
}
function runExpenseReport() {
  const s = document.getElementById('er-start').value;
  const e = document.getElementById('er-end').value;
  api(`/api/reports/expense-report?start_date=${s}&end_date=${e}`).then(d => {
    document.getElementById('er-output').textContent = JSON.stringify(d, null, 2);
  });
}

// Audits
function runAudits() {
  api('/api/audits').then(d => {
    const lines = d.map(x => `${x.passed ? '✅' : '❌'} ${x.check}  ${x.details ? '('+x.details+')' : ''}`);
    document.getElementById('audits-output').textContent = lines.join('\n');
  });
}
